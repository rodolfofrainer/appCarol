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
        const selectedItemQuantity = parseInt(itemQuantityInput.value); // Parse quantity as an integer
    
        // Check if the selected item is not "Select an item"
        if (selectedItemText !== "Select an item") {
            // Check if the item already exists in the selectedItems array
            const existingItemIndex = selectedItems.findIndex(item => item.startsWith(selectedItemText));
    
            if (existingItemIndex !== -1) {
                // Item already exists, update its quantity
                const existingItem = selectedItems[existingItemIndex];
                const [, existingQuantity] = existingItem.split(" - ");
                const newQuantity = parseInt(existingQuantity) + selectedItemQuantity;
    
                // Update the item in the array
                selectedItems[existingItemIndex] = `${selectedItemText} - ${newQuantity}`;
                
                // Update the item in the list
                const existingListItem = itemsList.children[existingItemIndex];
                existingListItem.textContent = `${selectedItemText} - ${newQuantity}`;
            } else {
                // Item doesn't exist, add it to the array
                const newItemText = `${selectedItemText} - ${selectedItemQuantity}`;
                selectedItems.push(newItemText);
    
                const newItem = document.createElement("li");
                newItem.textContent = newItemText;
                itemsList.appendChild(newItem);
            }
    
            console.log(selectedItems); // Debug
        } else {
            // Handle the case where "Select an item" is selected
            // You can show an alert or perform any other action here
            console.log("Please select a valid item.");
        }
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
