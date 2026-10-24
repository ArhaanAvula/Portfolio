function checkScamLink(document) {
    console.log("Content script is successfully running!");
    console.log("Content script loaded.");
    console.log("Current URL:", window.location.href);
    console.log("Document:", document);

    async function isScamLink(url) {
        const data = { "url": url };
        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            const result = await response.json();
            console.log(result);
            console.log('Prediction result:', result.prediction);
            return result.prediction;
        } catch (error) {
            console.error('Error:', error);
            return false; // consider safe on error
        }
    }

    async function processLinks() {
        var links = document.getElementsByTagName("a");
        for (var i = 0; i < links.length; i++) {
            if (links[i].href) {
                const prediction = await isScamLink(links[i].href);
                if (prediction) {
                    links[i].style.border = "5px solid red";
                    links[i].style.zIndex = "99999999999";
                }
            }
        }
    }

    const re = new RegExp("(https?:\\/\\/)?(www\\.)?[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}(\\:[0-9]{1,5})?(\\/[^\\s]*)?", "gi");

    async function bfs(document) {
        let visited = [];
        let queue = [document.body];
        while (queue.length > 0) {
            let el = queue.shift();
            if (!visited.includes(el)) {
                let combinedText = "";
                el.childNodes.forEach(node => {
                    if (node.nodeType === Node.TEXT_NODE) {
                        combinedText += node.textContent;
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        combinedText += node.textContent;
                    }
                });

                const matches = combinedText.match(re);
                console.log(matches);
                if (matches && matches.length == 1) {
                    for (const match of matches) {
                        const prediction = await isScamLink(match);
                        if (prediction) {
                            el.style.border = "5px solid red";
                            console.log("Styled element with scam link:", el);
                        }
                    }
                }
                visited.push(el);
                Array.from(el.children).forEach(child => queue.push(child));
            }
        }
    }

    async function runChecks() {
        await processLinks();
        await bfs(document);
    }

    runChecks();
}
checkScamLink(document);





// function checkScamLink(document) {
//     console.log("Content script is successfully running!");
//     // content.js
//     console.log("Content script loaded.");
//     console.log("Current URL:", window.location.href);
//     console.log("Document:", document);

//     function isScamLink(url) {
//         // Prepare data to send (you may need to convert the URL to features that the model expects)
//         const data = {
//             "url": url
//         };
    
//         // Make HTTP POST request to the Flask server - LOOK AT THIS CODE
//         fetch('http://127.0.0.1:5000/predict', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify(data),
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data)
//             console.log('Prediction result:', data.prediction);
//             return data.prediction;
//         })
//         .catch((error) => {
//             console.error('Error:', error);
//         });
//     }

//     // href is in <a href="example.com"></a> tag
//     var links = document.getElementsByTagName("a");
//     // console.log("Links:", links);
//     for (var i = 0; i < links.length; i++) {
//         if (links[i].href) {
//             if (isScamLink(links[i].href)) {
//                 links[i].style.border = "5px solid red";
//                 links[i].style.zIndex = "99999999999";
//             }
//         }
//     }

//     // Regular expression to detect potential URLs (covers basic and complex cases)
//     const re = new RegExp("(https?:\\/\\/)?(www\\.)?[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}(\\:[0-9]{1,5})?(\\/[^\\s]*)?", "gi");

//     // Breadth-first search
//     function bfs(document) {
//         let visited = [];
//         let queue = [document.body]; // to add .push() to remove .shift()
//         while (queue.length > 0) {
//             // Get next element.
//             el = queue.shift();
            
//             // Check that we have not yet seen this element.
//             if (!visited.includes(el)) {
//                 // Do the scam detection.

//                 // Combine text content from all child nodes (handling nested/fragments)
//                 let combinedText = "";
//                 el.childNodes.forEach(node => {
//                     if (node.nodeType === Node.TEXT_NODE) { 
//                         combinedText += node.textContent; // Add raw text
//                     } else if (node.nodeType === Node.ELEMENT_NODE) {
//                         combinedText += node.textContent; // Add text from child elements
//                     }
//                 });

//                 // Check if the combined text matches a URL
//                 const matches = combinedText.match(re); // Use .match() to get all matches
//                 console.log(matches);
//                 if (matches && matches.length == 1) {
//                     matches.forEach(match => {
//                         if (isScamLink(match)) {
//                             // Apply a red border to the parent element
//                             el.style.border = "5px solid red";
//                             console.log("Styled element with scam link:", el);
//                         }
//                     });
//                 }

//                 // Mark that we have seen this element and add all of its children to be processed.
//                 visited.push(el);
//                 Array.from(el.children).forEach(child => queue.push(child));
//             }
//         }
//     }

//     bfs(document);
// }
// checkScamLink(document);

// find some hash function, call it hash(value)
// TODO: does the document change?
// TODO: if it doesn't get a new one somehow
// var documentHash = hash(document);
// setInterval(function(){
//     const tempHash = hash(document);
//     if (tempHash != documentHash) {
//         documentHash = tempHash;
//         checkScamLink(document);
//     }
// }, 5000);


// const reloadButton = document.getElementById('reloadButton');
// console.log('btn', reloadButton);
// console.log("Content script loaded");
// if (reloadButton) {
//     reloadButton.addEventListener('click', function () {
//         console.log("Reload button clicked");
//         checkScamLink(mainDocument);
//     });
// }
