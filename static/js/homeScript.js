// Get CSRF token from a meta tag in your HTML template
function getCSRFToken() {
    const metaTag = document.querySelector('meta[name="csrf-token"]');
    if (metaTag) {
        return metaTag.getAttribute('content');
    }
    return null;
}

document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = getCSRFToken();
    const addButton = document.getElementById("add-to-list");
    const itemsList = document.getElementById("list-items");
    const itemNameSelect = document.getElementById("item-select");
    const itemQuantityInput = document.getElementById("item-quantity");
    const compareButton = document.getElementById("compare-button");

    const selectedItems = []; // Create an array to store selected items

    addButton.addEventListener("click", function () {
        const selectedItemText = itemNameSelect.options[itemNameSelect.selectedIndex].text;
        const selectedItemQuantity = itemQuantityInput.value;
        const newItemText = selectedItemText + " - " + selectedItemQuantity;

        selectedItems.push(newItemText); // Add the selected item to the array
        console.log(selectedItems); // Debug

        const newItem = document.createElement("li");
        newItem.textContent = newItemText;
        itemsList.appendChild(newItem);
    });

    compareButton.addEventListener("click", function () {
        const shoppingList = selectedItems; // Use the selectedItems array

        // Make an AJAX request to the server with the shopping list
        fetch('/compare/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
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
