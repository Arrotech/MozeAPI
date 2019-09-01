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

document.getElementById('getServices').onclick = () => {
        event.preventDefault();

        token = window.localStorage.getItem('token');
        let occupation = document.getElementById('occupation').value;

        fetch('http://localhost:5000/api/v1/add_services/' + occupation ,{
            method: 'GET',
            path: occupation,
            headers : {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token,
            },
        })
        .then((res) => res.json())
        .then((data) => {
            data.service.forEach(services => {
                let status = data['status'];
                let message = data['message'];
                const { service_provider, portfolio, occupation, location, img, cost } = services;
                output += `
                    <div className="stack">
                        <p className="par"><strong>Service Provider:</strong> ${services.service_provider}</p>
                        <p className="par"><Strong>Portfolio:</strong> ${services.portfolio}</p>
                        <p className="par"><strong>Occupation:</strong> ${services.occupation}</p>
                        <p className="par"><strong>Location:</strong> ${services.location}</p>
                        <p className="par"><strong>Image:</strong> ${services.img}</p>
                        <p className="par"><strong>Cost:</strong> ${services.cost}</p>
                    </div><br>
                    <br>
                `;
                if (status === '200'){
                    document.getElementById('output').innerHTML = output;
                }else{
                    raiseError(message);
                }
                });
                })
        .catch((err)=>{
            raiseError("Check your internet connection!");
            console.log(err);
        })
}
