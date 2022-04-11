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
    if(name === ""){
        name.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        $("#recipe_name").nextElementSibling.textContent = "*";
    }
    $("#recipe_name").value= name;

    if(description.value === ""){
        description.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        description.nextElementSibling.textContent = "*";
    }
    if(image.value === ""){
        image.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        image.nextElementSibling.textContent = "*";
    }


    if(ingredients.value === ""){
        ingredients.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        ingredients.nextElementSibling.textContent = "*";
    }
    if(servings.value === ""){
        servings.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        servings.nextElementSibling.textContent = "*";
    }
    if(prepare.value === ""){
        prepare.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        prepare.nextElementSibling.textContent = "*";
    }

    if(formIsComplete === true){
        $("#recipe_form").submit();
        alert("Your recipe has been submitted");
    }else {
        alert("Please complete form.")
    }

};

document.addEventListener("DOMContentLoaded",()=>{
    $("#submitButton").addEventListener("click", validateForm);

});