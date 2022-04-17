"use strict";

const $ = selector => document.querySelector(selector);



const validateForm =() =>{
    const name = $("#recipe_name").value.trim().toLowerCase();
    const description = $("#description");
    const ingredients = $("#recipe_ingredients");
    const prepare = $("#prepare");
    const servings = $("#servings");
    const image = $("#recipe_image");

    let formIsComplete = true;
    let msg = "";
    if(name === ""){
        $("#recipe_name").nextElementSibling.textContent = "Required section.";
        msg +="Enter recipe name\n";
        formIsComplete = false;
    }else{
        $("#recipe_name").nextElementSibling.textContent = "*";
    }
    $("#recipe_name").value= name;

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
    // $("#recipe_image").addEventListener("onchange", validateFileType);

});