"use strict";

const $ = selector => document.querySelector(selector);


const validateForm =() =>{
    const name = $("#recipe_name");
    const image = $("#recipe_image");
    const description = $("#description");
    const ingredients = $("#recipe_ingredients");
    const servings = $("#servings");
    const prepare = $("#prepare");

    let formIsComplete = true;
    if(name.value === ""){
        name.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
        alert("Enter name");
    }else{
        name.nextElementSibling.textContent = "*";
    }
    if(image.value === ""){
        image.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        image.nextElementSibling.textContent = "*";
    }
    if(description.value === ""){
        description.nextElementSibling.textContent = "Required section.";
        formIsComplete = false;
    }else{
        description.nextElementSibling.textContent = "*";
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
    }

};

document.addEventListener("DOMContentLoaded",()=>{
    $("#submitButton").addEventListener("click", validateForm);
    alert("DOM");
    console.log("ERRORRRR");

});