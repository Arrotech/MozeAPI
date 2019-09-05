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

        let occupation = document.getElementById('occupation').value;

        fetch(`https://arrotech-school-portal.herokuapp.com/api/v1/add_services/` + occupation ,{
            method: 'GET',
            path: occupation,
            headers : {
                Accept: 'application/json',
                'Content-Type': 'application/json',
            },
        })
        .then((res) => res.json())
        .then((data) => {
            data.service.forEach(services => {
                
                let status = data['status'];
                let message = data['message'];
                const { service_provider, portfolio, occupation, phone, location, img, cost } = services;
                // let result += ``;
                result += `
                    <div className="stack">
                        <p className="par">${services.service_provider}</p><hr>
                        <p className="par"><strong>${services.occupation}</strong></p><hr>
                        <p className="par" style="font-size:20px;"><strong>CALL:</strong><i><a href="tel:${services.phone}">${services.phone}</a></i></p><hr>
                        <p className="par" style="font-size:20px;"><i class="fa fa-map-marker" style="font-size:20px;color:red"></i> <strong>${services.location}</strong></p><hr>
                        <p className="par"><strong>${services.img}</strong></p><hr>
                        <p className="par" style="font-size:20px;"><strong>KSh: </strong><i><a>${services.cost}</a></i></p><hr>
                    </div><br><hr>
                    <br>
                `;
                if (status === '200'){
                    document.getElementById('result').innerHTML = result;
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
