document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(0));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(mailtype) {

  // Show compose view and hide other views
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';
  document.querySelector('#compose-body').value = '';
  

  // Clear out composition fields if new mail is being composed
  if (!mailtype) {
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
  }
  // Auto-fill composition fields when replying emails
  else {
    fetch(`/emails/${mailtype}`)
    .then(response => response.json())
    .then(email => {
        // Fetch receipients and subject of mail
        var receip = email.sender;
        var sub = email.subject;


        // Auto-fill fields during composition
        document.querySelector('#compose-recipients').value = receip;

        if (sub.charAt(0)==='R' && sub.charAt(1)==='e' && sub.charAt(2)===':') {
          document.querySelector('#compose-subject').value = sub;
        }
        else {
          document.querySelector('#compose-subject').value = 'Re: ' + sub;
        }
    });
  }

  // Send email
  document.querySelector('#compose-form').onsubmit = event => {
    event.preventDefault()

    // Get form inputs
    const rec = document.querySelector('#compose-recipients').value;
    const sub = document.querySelector('#compose-subject').value;
    const bod = document.querySelector('#compose-body').value;

    // Update API
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: rec,
        subject: sub,
        body: bod
      })
    })
      .then(response => response.json())
      .then(() => {
        load_mailbox('sent');
      });
      
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#read-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#title').innerHTML = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);

  // Clear Table body before fetching API
  document.querySelector('#box').innerHTML = '';

  // Display mailbox data
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...
      emails.forEach(element => {
        
        // Creating a row to display thumbnail of email
        const box = document.createElement('tr');

        // Changing color of thumbnail as per read status
        if (element.read) {
          box.style.backgroundColor = "WhiteSmoke";
        }
        else{
          box.style.backgroundColor = "white";
        }

        // Creating elements to fill the row
        const td1 = document.createElement('td');
        const td2 = document.createElement('td');
        const td3 = document.createElement('td');

        // Updating appropoiate values to those elements
        box.appendChild(td1);
        td1.innerHTML = element.sender;
        td1.style.verticalAlign = "middle";
        box.appendChild(td2);          
        td2.innerHTML = element.subject;
        td2.style.verticalAlign = "middle";
        box.appendChild(td3);       
        td3.innerHTML = element.timestamp;
        td3.style.verticalAlign = "middle";

        // Adding an archieve button
        if (mailbox != "sent"){

          const arch = document.createElement('td');
          const arch_but = document.createElement('button');
          arch_but.className = "btn btn-outline-dark";
          arch.appendChild(arch_but);
          arch.style.verticalAlign = "middle";
          box.appendChild(arch);
          if (element.archived) {
            arch_but.innerHTML = "UnArchieve";
          }
          else {
            arch_but.innerHTML = "Archieve";
          }
        }
        

        // Appending new row back to the table
        document.querySelector('#box').appendChild(box);

        // Managing what happens when that row is clicked
        box.addEventListener('click', event=> {

          if (event.target.className === "btn btn-outline-dark")
          {
            if (element.archived) {
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: false
                })
              })
              .then(() => {
                load_mailbox('inbox');
              })
            }
            else {
              fetch(`/emails/${element.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    archived: true
                })
              })
              .then(() => {
                load_mailbox('inbox');
              })
            }
            // event.stopImmediatePropagation();
          }
          else {
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#compose-view').style.display = 'none';
            document.querySelector('#read-view').style.display = 'block';
    
            document.querySelector('#read-subject').innerHTML = element.subject;
            document.querySelector('#read-sender').innerHTML = `by ${element.sender}`;
            document.querySelector('#read-time').innerHTML = element.timestamp;
            document.querySelector('#read-receiver').innerHTML = element.recipients;
            document.querySelector('#read-body').innerHTML = element.body;
            document.querySelector('#read-button').innerHTML = "Reply";

            // Adding on-click funtionality to the 'Archieve' button
            fetch(`/emails/${element.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
            })

            // Special case when reply button is clicked
            document.addEventListener('click', event=> {
              if (event.target.id === "read-button")
              {
                compose_email(element.id);
              }
            })
            }
        });
        
        console.log(element);
      });
  });
}