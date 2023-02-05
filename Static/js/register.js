// Vaidate the User Form

function validateForm() {
    var fieldsets = document.getElementsByClassName("form-row");
    var errorMessage = "";

    for (var i = 0; i < fieldsets.length; i++) {
        var firstName = fieldsets[i].getElementsByClassName("form-control")[0].value;
        var email = fieldsets[i].getElementsByClassName("form-control")[1].value;
        var homecomingTime = fieldsets[i].getElementsByClassName("form-control")[2].value;

        // Validate first name
        if (!firstName) {
        errorMessage += "First name is required for family member " + (i + 1) + ".\n";
        }

        // Validate email
        if (!email) {
        errorMessage += "Email is required for family member " + (i + 1) + ".\n";
        } else if (!/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
        errorMessage += "Email is not in the correct format for family member " + (i + 1) + ".\n";
        }

        // Validate homecoming time
        if (!homecomingTime) {
        errorMessage += "Homecoming time is required for family member " + (i + 1) + ".\n";
        }
    }

    // Display error message if there are any errors
    if (errorMessage) {
        alert(errorMessage);
        return false;
    }

    // If there are no errors, submit the form
    return true;
}

// Adds a new fieldset to add another family member
function addAnotherFamilyMember() {
    // Clone the first fieldset
    var firstFieldset = document.querySelector('fieldset.form-row');
    var newFieldset = firstFieldset.cloneNode(true);


    // Clear the values of the input fields
    newFieldset.querySelectorAll('input').forEach(function(input) {
        input.value = "";
    });

    // Append the new fieldset to the form
    document.getElementById('form-rows').appendChild(newFieldset);
}

// Deletes the fieldset of a given family member
function deleteFamilyMember(element) {
    if (document.querySelectorAll(".form-row").length > 1){
        $(element).closest("fieldset").remove();
    }
}

// Shows a loading symbol
function loading(){
    alert("Please wait while loading");
}

// Converts the form data into JSON and sends an AJAX request to the backend for submission
$(document).ready(function() {
    $('#user-registration-form').submit(function(event) {
        event.preventDefault();
        if (validateForm()){
            var familyMembers = [];
            $('#form-rows fieldset').each(function() {
            var member = {};
            member.first_name = $(this).find('input[name="first_name"]').val();
            member.email = $(this).find('input[name="email"]').val();
            member.homecoming_time = $(this).find('input[name="homecoming_time"]').val();
            member.holiday = $(this).find('select[name="holiday"]').val()
            familyMembers.push(member);
            });

            $.ajax({
                type: 'POST',
                url: "http://localhost:8080/register",
                data: JSON.stringify({ familyMembers: familyMembers }),
                contentType: 'application/json; charset=utf-8',
                success: function(data) {
                    console.log(data);
                    alert("Registration successful!");
                    window.location.href = "http://localhost:8080";
                    },
                error: function(xhr, status, error) {
                    console.error(error);
                    alert("An error occurred: " + error);
                }
            });
        }
    });
});