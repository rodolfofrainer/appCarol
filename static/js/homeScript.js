document.addEventListener("DOMContentLoaded", function () {
    var addButton = document.getElementById("add-to-list");
    var itemsList = document.getElementById("list-items");
    var itemNameSelect = document.getElementById("item-select");
    var itemQuantityInput = document.getElementById("item-quantity");
    var compareButton = document.getElementById("compare-button");

    addButton.addEventListener("click", function () {
        var selectedItemText = itemNameSelect.options[itemNameSelect.selectedIndex].text;
        var selectedItemQuantity = itemQuantityInput.value;
        var newItemText = selectedItemText + " - " + selectedItemQuantity;

        var newItem = document.createElement("li");
        newItem.textContent = newItemText;
        itemsList.appendChild(newItem);
    });

    compareButton.addEventListener("click", function () {
        var shoppingList = [];
        var listItems = itemsList.querySelectorAll("li");
        listItems.forEach(function (item) {
            shoppingList.push(item.textContent);
        });

        // Make an AJAX request to the server with the shopping list
        fetch('/compare/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token  // You need to obtain the CSRF token from your Django template
            },
            body: JSON.stringify({ shoppingList: shoppingList })
        })
        .then(response => response.json())
        .then(data => {
            // Handle the server's response, e.g., display the comparison results
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
