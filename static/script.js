document.addEventListener("DOMContentLoaded", function() {
    const bookTableBody = document.querySelector("#bookTable tbody");

    // Fetch and Display Books from Backend (via Flask)
    function loadBooks() {
        fetch("/books")
            .then(response => response.json())
            .then(data => {
                bookTableBody.innerHTML = "";
                data.forEach(book => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${book.title}</td>
                        <td>${book.author}</td>
                        <td>${book.publication_date}</td>
                        <td>${book.genre}</td>
                        <td><button class="deleteBtn" data-id="${book.id}">Delete</button></td>
                    `;
                    bookTableBody.appendChild(row);
                });

                // Add Delete Book Event
                document.querySelectorAll(".deleteBtn").forEach(button => {
                    button.addEventListener("click", function() {
                        deleteBook(this.getAttribute("data-id"));
                    });
                });
            });
    }

    // Delete Book
    function deleteBook(bookId) {
        fetch(`/books/${bookId}`, {
            method: "DELETE"
        }).then(() => {
            loadBooks();
        });
    }

    // Initial Load
    loadBooks();
});
