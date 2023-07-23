// Variable to store csrf token once, for all the fetches
let csrftoken;


document.addEventListener('DOMContentLoaded', function() {
    // Hide error messages after 7 seconds
    if (message)  {
        setTimeout(()=> {
            document.querySelector('.message').remove()
        }, 7000)
    }

    // Get csrf token
    csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Check if user is logged in to display his follow data
    if (logged) {

        // Query the number of followers and following by fetching.
        fetch(`/followdata/${visited_user}`, {
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            },
        })
        .then (response => {
            return response.json()
        })
        .then (data => {

            // Add a follow button if our user is visiting someone else's profile
            if (visited_user != current_user){

                // Make the follow button's padding dependable on username's width
                const box = document.querySelector('#instant-follow-switch');
                const title_width = document.querySelector('#username').clientWidth - 48.625;
                box.setAttribute('style', `padding-Left: ${title_width}px`);

                const label = document.createElement('label');
                label.className = "follow-switch";
                
                const checker = document.createElement('input');
                checker.type = "checkbox";
                checker.id = "profile-follow-button";

                const span = document.createElement('span');
                span.className = "slider";

                if (data.status) {
                    checker.checked = true;
                }
                else {
                    checker.checked = false
                }

                label.appendChild(checker);
                label.appendChild(span);
                box.appendChild(label);

                // Make the follow button functional
                checker.addEventListener('click', () => follow_button_clicked(current_user, visited_user));
            }

            // Load followers and following info
            load_follow_data(data);
        })
    }
    else {
        // IF the user is not logged in, load login and register menu
        load_authentication_options();
    }
    
})


// OnClick functionality of follow button
function follow_button_clicked(c, v) {

    // Update the follower status through API
    fetch(`/follow`, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            follower: c,
            following: v
        })
    })
    .then(response => {
        response.json()
    })
    .then( ()=> {
        // // Query the updated number of followers and following by fetching.
        fetch(`/followdata/${visited_user}`, {
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            },
        })
        .then (response => {
            return response.json()
        })
        .then (data => {
            load_follow_data(data);
        })
    })
}


// Render the received following data
function load_following(data) {
    const box = document.querySelector('#follow-data-display');

    const wrapper = document.createElement('div');
    wrapper.className = 'right-wrapper';
    wrapper.style.zIndex = '1';

    const inner_box = document.createElement('div');
    inner_box.className = 'navlink-popup';

    var head = document.createElement('h3');
    head.innerHTML = `${data.following_count} following`;

    inner_box.appendChild(head);

    const following = data.following;

    // Create separate spaces for every user
    following.forEach(follower => {
        const follow_thumb = document.createElement('a');
        follow_thumb.className = 'follow-thumb';

        if (follower.id == current_user){
            follow_thumb.href = `/`;
        }
        else {
            follow_thumb.href = `/user/${follower.id}`;
        }

        const push_left = document.createElement('div');
        push_left.className = 'push-left';

        const img = document.createElement('img');
        if (follower.pfp === "None") {
            img.src = static.concat("network/nopfp.png"); //add static prefix
        }
        else {
            img.src = media.concat(follower.pfp); //add media prefix
        }
        img.className = 'user-pfp-shrink';

        const name = document.createElement('span');
        name.className = 'following-name';
        name.innerHTML = follower.username;

        // Add the follow button for each user unless (s)he's same as current user
        if (follower.id != current_user) {
            const label = document.createElement('label');
            label.className = 'follow-switch push-right';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            if (follower.status) {
                checkbox.checked = true;
            }
            else {
                checkbox.checked = false
            }

            const span = document.createElement('span');
            span.className = 'slider';

            label.appendChild(checkbox);
            label.appendChild(span);
            push_left.appendChild(img);
            push_left.appendChild(name);
            follow_thumb.appendChild(push_left);
            follow_thumb.appendChild(label);

            // Make that follow button functional
            checkbox.addEventListener('click', () => follow_button_clicked(current_user, follower.id));
        }
        else {
            // User is same as the one being displayed, thus no follow button
            push_left.appendChild(img);
            push_left.appendChild(name);
            follow_thumb.appendChild(push_left);
        }
        inner_box.appendChild(follow_thumb);
    });

    // Append everything into the overlay
    wrapper.appendChild(inner_box);
    box.appendChild(wrapper);

    // Close the overlay whenever user clicks outside
    document.querySelector('#followers').addEventListener('click', ()=> wrapper.remove());
    onClickOutside(box, () => wrapper.remove());
}


// Fill followers overlay on clicking
function load_followers(data) {
    const box = document.querySelector('#follow-data-display');
    
    const wrapper = document.createElement('div');
    wrapper.className = 'left-wrapper';
    wrapper.style.zIndex = '1';

    const inner_box = document.createElement('div');
    inner_box.className = 'navlink-popup';

    var head = document.createElement('h3');
    head.style.alignSelf = 'flex-end';
    if (data.follower_count === 1) {
        head.innerHTML = '1 follower';
    }
    else {
        head.innerHTML = `${data.follower_count} followers`;
    }
    inner_box.appendChild(head);

    const followers = data.followers;

    // Display every follower
    followers.forEach(follower => {
        const follow_thumb = document.createElement('a');
        follow_thumb.className = 'follow-thumb';
        if (follower.id == current_user){
            follow_thumb.href = `/`;
        }
        else {
            follow_thumb.href = `/user/${follower.id}`;
        }

        const push_left = document.createElement('div');
        push_left.className = 'push-left';

        const img = document.createElement('img');
        if (follower.pfp === "None") {
            img.src = static.concat("network/nopfp.png"); //add static prefix
        }
        else {
            img.src = media.concat(follower.pfp); //add media prefix
        }
        img.className = 'user-pfp-shrink';

        const name = document.createElement('span');
        name.className = 'following-name';
        name.innerHTML = follower.username;

        // Add the follow button for each user unless (s)he's same as current user
        if (follower.id != current_user) {
            const label = document.createElement('label');
            label.className = 'follow-switch push-right';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            if (follower.status) {
                checkbox.checked = true;
            }
            else {
                checkbox.checked = false
            }

            const span = document.createElement('span');
            span.className = 'slider';

            label.appendChild(checkbox);
            label.appendChild(span);
            push_left.appendChild(img);
            push_left.appendChild(name);
            follow_thumb.appendChild(push_left);
            follow_thumb.appendChild(label);

            // Make the follow button functional
            checkbox.addEventListener('click', () => follow_button_clicked(current_user, follower.id));
        }
        else {
            // No following button when user sees themselves
            push_left.appendChild(img);
            push_left.appendChild(name);
            follow_thumb.appendChild(push_left);
        } 
        inner_box.appendChild(follow_thumb);
    });

    // Append everything into the followers overlay
    wrapper.appendChild(inner_box);
    box.appendChild(wrapper);

    // Close whenever user clicks outside the overlay
    document.querySelector('#following').addEventListener('click', ()=> wrapper.remove());
    onClickOutside(box, () => wrapper.remove());
}


// Display number of followers and followings
function load_follow_data(data) {
    const navs = document.querySelector('#follow-data-display');
    navs.innerHTML = '';

    var followers_title = document.createElement('h3');
    followers_title.id = 'followers';
    followers_title.className = 'navlink follow';
    if (data.follower_count === 1)
    {
        followers_title.innerHTML = `1 follower`;
    }
    else {
        followers_title.innerHTML = `${data.follower_count} followers`;
    }

    var following_title = document.createElement('h3');
    following_title.className = 'navlink follow';
    following_title.id = 'following';
    following_title.innerHTML = `${data.following_count} following`;

    navs.appendChild(followers_title)
    navs.appendChild(following_title)

    // Add interaction functionality to above data
    if (data.follower_count) {
        followers_title.addEventListener('click', () => load_followers(data));
    }
    if (data.following_count) {;
        following_title.addEventListener('click', () => load_following(data));
    }
}


// Funciton to detect any click outside the first parameter and then implement the second parameter
function onClickOutside(a, b) {
    document.addEventListener('click', event => {
        if (!a.contains(event.target)) b();
    });
}


// Update likes on a post asynchronously through fetch
function liked(post, key) {
    let span2;

    // If key is 2, user liked through full screen post thus both full-screen and post thumbnail stats need to be updated
    if (key === 2) {
        const icon = document.querySelector(`#like-open-icon-${post}`);
        const link = icon.getAttribute('src');
        const span = document.querySelector(`#like-open-stat-${post}`);

        // Change like icon accordingly when a post is (dis)liked
        if (link === static.concat('network/like.svg')) {
            icon.src = `${static.concat('network/liked.svg')}`;
        }
        else {
            icon.src = `${static.concat('network/like.svg')}`;
        }
        span2 = span;
    }

    // If key isn't 2, only the post thumbnail menu needs to be updated
    const icon = document.querySelector(`#like-icon-${post}`);
    const link = icon.getAttribute('src');
    const span = document.querySelector(`#like-stat-${post}`);

    // Change like icon accordingly when a post is (dis)liked
    if (link === static.concat('network/like.svg')) {
        icon.src = `${static.concat('network/liked.svg')}`;
    }
    else {
        icon.src = `${static.concat('network/like.svg')}`;
    }

    // Update the like status on server
    fetch(`/like`, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            liked: post
        })
    })
    .then(response => 
        response.json()
    )
    .then(response => {
        // Span number of likes on post accordingly based on updated likes received from the server
        span.innerHTML = '';
        if (response.likes === 1)
        {
            span.innerHTML = '1 like';
            if (key === 2) {
                span2.innerHTML = '';
                span2.innerHTML = '1 like';
            }
        }
        else {
            span.innerHTML = `${response.likes} likes`;
            if (key === 2) {
                span2.innerHTML = '';
                span2.innerHTML = `${response.likes} likes`;
            }
        }
    })
}


// Load the authentication options when the user is not logged in
function load_authentication_options() {
    const navs = document.querySelector('#follow-data-display');
    navs.innerHTML = '';

    var login = document.createElement('h3');
    login.id = 'login';
    login.classList.add('navlink', 'login');
    login.innerHTML = 'Login'

    var register = document.createElement('h3');
    register.classList.add('navlink', 'login');
    register.id = 'register';
    register.innerHTML = `Register`;

    navs.appendChild(login)
    navs.appendChild(register)

    // Make both login and register headings functional
    login.addEventListener('click', () => login_menu());
    register.addEventListener('click', () => register_menu());
}


// Dynamically render the login overlay menu when login is clicked
function login_menu() {
    const box = document.querySelector('#follow-data-display');

    const wrapper = document.createElement('div');
    wrapper.className = 'left-wrapper';
    wrapper.style.overflow = 'visible';
    wrapper.style.zIndex = '1';

    const inner_box = document.createElement('div');
    inner_box.className = 'navlink-popup';

    const form  = document.createElement('form');
    form.action = '/login';
    form.method = 'post';
    form.className = 'navlink-popup';

    // Make the title centrally aligned for mobile phones
    const head = document.createElement('h3');
    head.innerHTML = 'Login';
    head.style.marginBottom = '1.8rem';
    if (window.innerWidth <= 600) {
        head.style.alignSelf = 'center';
    }
    else {
        head.style.alignSelf = 'flex-end';
    }

    const token = document.createElement('input');
    token.name = 'csrfmiddlewaretoken';
    token.type = 'hidden';
    token.value = csrftoken;
    
    const username = document.createElement('input');
    username.className = 'login-input';
    username.placeholder = 'Username';
    username.name = 'username';
    username.type = 'text';
    username.required = 'True';

    const password = document.createElement('input');
    password.className = 'login-input';
    password.placeholder = 'Password';
    password.name = 'password';
    password.type = 'password';
    password.required = 'True';

    const button = document.createElement('button');
    button.className = 'sub-button';
    button.value = 'login';
    button.innerHTML = 'L O G I N';

    form.appendChild(token);
    form.appendChild(username);
    form.appendChild(password);
    form.appendChild(button);
    inner_box.appendChild(head);
    inner_box.appendChild(form);
    wrapper.appendChild(inner_box);
    box.appendChild(wrapper);

    // Close whenever user clicks outside the overlay
    document.querySelector('#register').addEventListener('click', ()=> wrapper.remove());
    onClickOutside(box, () => wrapper.remove());
}


// Dynamically render the register overlay menu when register is clicked
function register_menu() {
    const box = document.querySelector('#follow-data-display');

    const wrapper = document.createElement('div');
    wrapper.className = 'right-wrapper';
    wrapper.style.overflow = 'visible';
    wrapper.style.height = 'auto';
    wrapper.style.maxHeight = 'none';
    wrapper.style.zIndex = '1';

    const inner_box = document.createElement('div');
    inner_box.className = 'navlink-popup';

    const form  = document.createElement('form');
    form.action = '/register';
    form.method = 'post';
    form.className = 'navlink-popup';
    form.enctype = 'multipart/form-data';

    // Make the title centrally aligned for mobile phones
    const head = document.createElement('h3');
    head.style.alignSelf = 'flex-start';
    head.innerHTML = 'Register';
    head.style.marginBottom = '1.8rem';
    if (window.innerWidth <= 600) {
        head.style.alignSelf = 'center';
    }
    else {
        head.style.alignSelf = 'flex-start';
    }

    const token = document.createElement('input');
    token.name = 'csrfmiddlewaretoken';
    token.type = 'hidden';
    token.value = csrftoken;

    const email = document.createElement('input');
    email.className = 'login-input';
    email.placeholder = 'Email address *';
    email.name = 'email';
    email.type = 'email';
    email.required = 'True';
    
    const username = document.createElement('input');
    username.className = 'login-input';
    username.placeholder = 'Username *';
    username.name = 'username';
    username.type = 'text';
    username.required = 'True';

    const password = document.createElement('input');
    password.className = 'login-input';
    password.placeholder = 'Password *';
    password.name = 'password';
    password.type = 'password';
    password.required = 'True';

    const repassword = document.createElement('input');
    repassword.className = 'login-input';
    repassword.placeholder = 're-enter Password *';
    repassword.name = 'confirmation';
    repassword.type = 'password';
    repassword.required = 'True';

    const img_div = document.createElement('div');
    img_div.className = 'pfp-input';

    const label = document.createElement('label');
    label.setAttribute('for', 'files');
    label.innerHTML = 'Profile Picture';
    label.style.marginBottom = '0';

    const pfp = document.createElement('input');
    pfp.type = 'file';
    pfp.style.opacity = '0';
    pfp.id = 'files';
    pfp.value = '';
    pfp.accept = 'image/*';
    pfp.name = 'pfp';
    pfp.style.position = 'absolute';

    const button = document.createElement('button');
    button.className = 'sub-button';
    button.value = 'register';
    button.innerHTML = 'R E G I S T E R';

    img_div.appendChild(label);
    img_div.appendChild(pfp);

    form.appendChild(token);
    form.appendChild(email);
    form.appendChild(username);
    form.appendChild(password);
    form.appendChild(repassword);
    form.appendChild(img_div);
    form.appendChild(button);

    inner_box.appendChild(head);
    inner_box.appendChild(form);

    wrapper.appendChild(inner_box);
    box.appendChild(wrapper);

    // Close whenever user clicks outside the overlay
    document.querySelector('#login').addEventListener('click', ()=> wrapper.remove());
    onClickOutside(box, () => wrapper.remove());

    // Display name of image chosen
    pfp.addEventListener('change', ()=> {
        const filename = pfp.files[0]?.name;
        label.innerHTML = filename ?? "Upload an image";
    });
}


// Function offering both edit post and create post functionality through same UI, based on what element what clicked to call
function edit(event, id) {

    // Scroll to the top of the page where hover opens
    window.scrollTo({top: 0, behavior: 'smooth'});

    // Create the shared layout
    const box = document.createElement('div');
    box.className = 'post-box';
    box.style.zIndex = '1';

    const head = document.createElement('div');
    head.className = 'post-open-head';

    const info = document.createElement('div');
    info.className = 'post-open-info';
    
    const pfp = document.createElement('img');
    pfp.className = 'poster-pfp';

    const name = document.createElement('span');
    name.className = 'post-open-name';

    const datetime = document.createElement('span');
    datetime.className = 'post-open-datetime';

    const icons = document.createElement('div');
    icons.className = 'post-open-icons';
    icons.style.paddingBottom = '0.4rem';

    const tick = document.createElement('img');
    tick.className = 'like-icon';
    tick.src = static.concat('network/save.svg');

    const line = document.createElement('div');
    line.className = 'line';

    const content = document.createElement('form');
    content.style.paddingLeft = '3vw';
    content.style.paddingRight = '3vw';
    content.className = 'post-open-content';
    content.method = 'post';
    content.enctype = 'multipart/form-data';

    const token = document.createElement('input');
    token.name = 'csrfmiddlewaretoken';
    token.type = 'hidden';
    token.value = csrftoken;

    const img_div = document.createElement('div');
    img_div.className = 'login-input';

    const img_label = document.createElement('label');
    img_label.setAttribute('for', 'files');
    img_label.innerHTML = 'Upload an image';
    img_label.style.marginBottom = '0';
    img_label.style.width = '-webkit-fill-available';

    const img_input = document.createElement('input');
    img_input.type = 'file';
    img_input.style.opacity = '0';
    img_input.id = 'files';
    img_input.accept = 'image/*';
    img_input.name = 'image';
    img_input.style.position = 'absolute';
    img_input.style.width = '-webkit-fill-available';

    const caption = document.createElement('textarea');
    caption.className = 'login-input';
    caption.placeholder = "What's on your mind!";
    caption.rows = '25';
    caption.name = 'content';

    const post_id = document.createElement('input');
    post_id.value = id;
    post_id.style.display = 'none';
    post_id.name = 'post_id';

    // Check whether the function is called for creating a post or editing a post and render the page accordingly
    if (event.target.innerHTML === 'Create') {
        if (who_pfp) {
            pfp.src = media.concat(who_pfp);
        }
        else {
            pfp.src = static.concat('network/nopfp.png');
        }
        name.innerHTML = who;
        datetime.innerHTML = current_time;
        content.action = create;

        img_div.appendChild(img_label);
        img_div.appendChild(img_input);

        content.appendChild(token)
        content.appendChild(img_div);
        content.appendChild(caption);

        info.appendChild(pfp);
        info.appendChild(name);
        info.appendChild(datetime);

        icons.appendChild(tick);

        head.appendChild(info);
        head.appendChild(icons);

        box.appendChild(head);
        box.appendChild(line);
        box.appendChild(content);

        // Display the overlay
        document.querySelector('body').style.overflow = 'hidden';
        console.log(box);
        document.querySelector('.navs').appendChild(box);

        // Submit the form
        tick.addEventListener('click', () => content.submit());
        
        // Close the overlay
        document.addEventListener('click', () => onClickOutside(box, () => {
            box.remove();
            document.querySelector('body').style.overflow = 'scroll';
        }));

        // Display name of image chosen
        img_input.addEventListener('change', ()=> {
            const filename = img_input.files[0]?.name;
            img_label.innerHTML = filename ?? "Upload an image";
        });
        return;
    }
    else {
        console.log('entered else');
        fetch(`/post`, {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                id: id
            })
        })
        .then(response => 
            response.json()
        )
        .then(post => {
            if (post.pfp) {
                pfp.src = media.concat(post.pfp);
            }
            else {
                pfp.src = static.concat('network/nopfp.png');
            }

            name.innerHTML = post.owner_name
            datetime.innerHTML = post.info;
            content.action = edit_url;

            if (post.image) {
                img_label.innerHTML = post.image.slice(6);
            }
            if (post.content) {
                caption.innerHTML = post.content;
            }
        })
        .then( () => {
            img_div.appendChild(img_label);
            img_div.appendChild(img_input);

            content.appendChild(token)
            content.appendChild(img_div);
            content.appendChild(caption);
            content.appendChild(post_id);

            info.appendChild(pfp);
            info.appendChild(name);
            info.appendChild(datetime);

            icons.appendChild(tick);

            head.appendChild(info);
            head.appendChild(icons);

            box.appendChild(head);
            box.appendChild(line);
            box.appendChild(content);

            // Display the overlay
            document.querySelector('body').style.overflow = 'hidden';   
            console.log(box);
            document.querySelector('.feed').appendChild(box);
            
            onClickOutside(box, () => {
                box.remove();
                document.querySelector('body').style.overflow = 'scroll';
            });

            // Display name of image chosen
            img_input.addEventListener('change', ()=> {
                const filename = img_input.files[0]?.name;
                img_label.innerHTML = filename ?? "Upload an image";
            });

            //Submit the form
            tick.addEventListener('click', () => content.submit());
            
        });
    }
}


// Load the post as an overlay
function load_post(event, id) {
    // Stopping if the user clicked on some child element and not actual post
    if ((event.target.className === 'like-icon') || (event.target.className === 'poster-pfp') || (event.target.className === 'poster-name') || (event.target.className === 'poster-thumb') || (event.target.className === 'like-icon edit')){
        return event.stopPropagation();
    }

    // Scroll the window to top to open overlay
    window.scrollTo({top: 0, behavior: 'smooth'});

    // Fetch post data from server through API through ajax request
    fetch(`/post`, {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => 
        response.json()
    )
    .then(post => {

        const box = document.createElement('div');
        box.className = 'post-box';
        box.style.zIndex = '1';

        const head = document.createElement('div');
        head.className = 'post-open-head';

        const info = document.createElement('div');
        info.className = 'post-open-info';
        
        const pfp = document.createElement('img');
        pfp.className = 'poster-pfp';
        if (post.pfp) {
            pfp.src = media.concat(post.pfp);
        }
        else {
            pfp.src = static.concat('network/nopfp.png');
        }

        const name = document.createElement('span');
        name.className = 'post-open-name';
        name.innerHTML = post.owner_name

        const datetime = document.createElement('span');
        datetime.className = 'post-open-datetime';
        datetime.innerHTML = post.info;

        const icons = document.createElement('div');
        icons.className = 'post-open-icons';

        const like_data = document.createElement('div');
        like_data.className = 'post-likes';
        like_data.id = `like-open-stat-${ post.id }`;
        like_data.style.marginRight = '0.4rem';
        like_data.style.paddingBottom = '0.4rem';
        if (post.likes == 1) {
            like_data.innerHTML = '1 like';
        }
        else {
            like_data.innerHTML = `${post.likes} likes`;
        }

        const like = document.createElement('img');
        like.className = 'like-icon';
        like.style.marginRight = '1.2rem';
        like.id = `like-open-icon-${ post.id }`;
        let x;
        if (post.like_status) {
            x = static.concat('network/liked.svg');
        }
        else {
            x = static.concat('network/like.svg');
        }
        like.setAttribute("src", x);
        
        const edit_icon = document.createElement('img');
        edit_icon.className = 'like-icon';
        edit_icon.src = static.concat('network/edit.svg');

        const line = document.createElement('div');
        line.className = 'line';

        const content = document.createElement('div');
        content.className = 'post-open-content';

        if (post.image) {
            const post_img = document.createElement('img');
            post_img.className = 'post-open-image';
            post_img.src = media.concat(post.image);
            post_img.style.maxWidth = `${window.innerWidth / 2.23}px`;
            content.appendChild(post_img);
        }
        
        const post_caption = document.createElement('div');
        post_caption.className = 'post-open-caption';
        post_caption.innerHTML = post.content;
        content.appendChild(post_caption);

        info.appendChild(pfp);
        info.appendChild(name);
        info.appendChild(datetime);

        // Render post responsively
        if (window.innerWidth <= 600) {
            if (logged) {
                if (post.owner_id === Number(current_user)) {
                    icons.appendChild(like);
                    icons.appendChild(edit_icon);
                }
                else {
                    console.log("Entered else");
                    icons.appendChild(like_data);
                    like.style.marginRight = 0;
                    icons.appendChild(like);
                }
            }
            else {
                icons.appendChild(like_data);
            }
        }
        else {
            icons.appendChild(like_data);
            if (logged) {
                if (post.owner_id === Number(current_user)) {
                    icons.appendChild(like);
                    icons.appendChild(edit_icon);
                }
                else {
                    console.log("Entered else");
                    like.style.marginRight = 0;
                    icons.appendChild(like);
                }
            }
        }

        head.appendChild(info);
        head.appendChild(icons);

        box.appendChild(head);
        box.appendChild(line);
        box.appendChild(content);

        // Stop overflow on body to keep the overlay fixed
        document.querySelector('body').style.overflow = 'hidden';
        document.querySelector('.feed').appendChild(box);
        
        // Close post overlay when anything outside of it is clicked
        onClickOutside(box, () => {
            box.remove();
            document.querySelector('body').style.overflow = 'scroll';
        });

        // Make the like and edit icon on the post functional
        like.addEventListener('click', ()=> liked(post.id, 2));
        edit_icon.addEventListener('click', ()=> edit(event, post.id));
    })
}