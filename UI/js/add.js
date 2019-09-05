document.getElementById('postServices').addEventListener('submit', postServices);

    function callToast() {

        var x = document.getElementById("snackbar");
        x.className = "show";
        setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
    }

    function onSuccess(msg){

        document.getElementById('snackbar').innerText = msg
        callToast();
    }

    function raiseError(msg){

        document.getElementById('snackbar').innerText = msg
        callToast();
    }

    function postServices(event){
            event.preventDefault();

            token = window.localStorage.getItem('token');

            let service_provider = document.getElementById('service_provider').value;
            let portfolio = document.getElementById('portfolio').value;
            let occupation = document.getElementById('occupation').value;
            let phone = document.getElementById('phone').value;
            let location = document.getElementById('location').value;
            let img = document.getElementById('img').value;
            let cost = document.getElementById('cost').value;

            fetch('https://arrotech-school-portal.herokuapp.com/api/v1/add_services', {
                method: 'POST',
                headers : {
                Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
                body:JSON.stringify({service_provider:service_provider, portfolio:portfolio, occupation:occupation, phone:phone, location:location, img:img, cost:cost})
            }).then((res) => res.json())
            .then((data) =>  {

                console.log(data);
                let status = data['status'];
                let message = data['message'];
                if (status === '201'){
                    onSuccess('Service added successsfully');
                }else{
                    raiseError(message);
                }

            })
            .catch((err)=>{
                raiseError("Check your internet connection!");
                console.log(err);
            })
        }
