    // Add AJAX script for real-time search
    $(document).ready(function() {
        var searchInput = $('#searchInput');
        var searchResults = $('#searchResults');

        // Handle input in the search field
        searchInput.on('input', function() {
            var searchQuery = searchInput.val().trim(); // Trim whitespace
            if (searchQuery === '') {
                clearSearchResults();
            } else {
                sendSearchRequest(searchQuery);
            }
        });

        // Handle click outside the search input to clear results
        $(document).on('click', function(event) {
            if (!searchInput.is(event.target) && !searchResults.is(event.target) && searchResults.has(event.target).length === 0) {
                clearSearchResults();
            }
        });

        function sendSearchRequest(searchQuery) {
            $.ajax({
                type: 'POST',
                url: '/search',
                data: {search_query: searchQuery},
                success: function(data) {
                    displaySearchResults(data);
                },
                error: function(error) {
                    console.error('Error:', error);
                }
            });
        }

        function displaySearchResults(results) {
            searchResults.empty();
            if (results.length === 0) {
                searchResults.append('<li class="list-group-item">No results found</li>');
            } else {
                $.each(results, function(index, result) {
                    image_path = `<img src=${result.image_path} class='img-thumbnail' width='64px' height='64px'>`
                    searchResults.append(`<li class="list-group-item">
                    <div class="d-flex">
                        <div class="container">
                            ${image_path}
                            <a href="/view-item/${result.prod_code}'
                            <p><strong>${result.name}</strong></p>
                            <p>Price: ${result.price} Rs</p>
                        </div>
                    </div>
                    </li>`);
                });
            }
        }

        function clearSearchResults() {
            searchResults.empty();
        }
    });
