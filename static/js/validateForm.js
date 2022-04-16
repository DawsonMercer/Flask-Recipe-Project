"use strict";

const $ = selector => document.querySelector(selector);


const validateForm =() =>{
    const name = $("#exampleFormControlInput1").value.trim().toLowerCase();
    const description = $("#exampleFormControlInput5");
    const ingredients = $("#exampleFormControlTextarea1");
    const prepare = $("#exampleFormControlInput2");
    const servings = $("#exampleFormControlInput3");
    const image = $("#exampleFormControlFile1");

    let formIsComplete = true;
    let msg = "";
    if(name === ""){
        $("#exampleFormControlInput1").nextElementSibling.textContent = "Required section.";
        msg +="Enter recipe name\n";
        formIsComplete = false;
    }else{
        $("#exampleFormControlInput1").nextElementSibling.textContent = "*";
    }
    $("#exampleFormControlInput1").value= name;

    if(description.value === ""){
        description.nextElementSibling.textContent = "Required section.";
        msg +="Enter recipe description\n";
        formIsComplete = false;
    }else{
        description.nextElementSibling.textContent = "*";
    }
    if(image.value === ""){
        image.nextElementSibling.textContent = "Required section.";
        msg +="Enter recipe image\n";
        formIsComplete = false;
    }else{
        image.nextElementSibling.textContent = "*";
    }


    if(ingredients.value === ""){
        ingredients.nextElementSibling.textContent = "Required section.";
        msg +="Enter ingredients\n";
        formIsComplete = false;
    }else{
        ingredients.nextElementSibling.textContent = "*";
    }
    if(servings.value === ""){
        servings.nextElementSibling.textContent = "Required section.";
        msg +="Enter number of servings\n";
        formIsComplete = false;
    }else{
        servings.nextElementSibling.textContent = "*";
    }
    if(prepare.value === ""){
        prepare.nextElementSibling.textContent = "Required section.";
        msg +="Enter prep info\n";
        formIsComplete = false;
    }else{
        prepare.nextElementSibling.textContent = "*";
    }

    if(formIsComplete === true){
        $("#recipe_form").submit();
        alert("Your recipe has been submitted");
    }else {
        alert("Please complete form.")
        // alert(msg);
    }

};

document.addEventListener("DOMContentLoaded",()=>{
    $("#submitButton").addEventListener("click", validateForm);

});