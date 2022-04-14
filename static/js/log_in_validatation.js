"use strict";

const $ = selector => document.querySelector(selector);


const validateUser = () =>{
    const username = $("#user").value.trim().toLowerCase();
    const password = $("#password").value.trim();
    let formIsComplete = false;
    alert("Your log in is being processed")

}


document.addEventListener("DOMContentLoaded",()=>{
    $("#clickMe").addEventListener("click", validateUser);

});