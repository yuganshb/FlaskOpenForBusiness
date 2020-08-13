document.addEventListener("DOMContentLoaded", function(){
document.getElementById("btnStart").addEventListener("click", setup);
});
function setup(){
    let name = document.getElementById('inputName');
    let mobileNumber = document.getElementById('mobileNumber');
    let aadharNumber = document.getElementById('aadharNumber');
    let numberOfPeople = document.getElementById('numberOfPeople');

    let data = {
        "name": name.value,
        "mobileNumber" : mobileNumber.value,
        "aadharNumber" : aadharNumber.value,
        "numberOfPeople" : numberOfPeople.value
        };

    fetch("/generateUUID", {
        method: "post",
        body: data,
        headers: {
            'Content-Type': 'application/json',
        }
   }).then(response => response.text())
    .then(text => console.log(text));;

   console.log("response", response);
   if(response.ok){
    let text = await response.text();
    console.log(text);
   }
   console.log(data, uuid);
}