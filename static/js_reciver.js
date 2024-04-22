
const socket = new WebSocket(`ws://localhost:8000/ws/${document.URL.split('/').pop()}`);
const button = document.querySelector('button')
const input = document.querySelector('input')
const h1 = document.querySelector('h1')



button.addEventListener('click',e =>{
    socket.send(input.value)
})



socket.addEventListener('open', function (event) {
    console.log('Connected to WebSocket server');
});

socket.addEventListener('message', function (event) {
    console.log(event.data);
    h1.innerHTML = event.data
    // socket.send('Hello, WebSocket Server!');
});

// socket.addEventListener('close', function (event) {
//     console.log('Disconnected from WebSocket server');
// });


// socket.addEventListener('error', function (event) {
//     console.error('WebSocket error:', event);
// });

// addEventListener("beforeunload", e => {
//     socket.close()
// })
