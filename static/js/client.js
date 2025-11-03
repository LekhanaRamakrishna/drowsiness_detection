// static/js/client.js
const socket = io(); // connects to same origin
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const earVal = document.getElementById('earVal');
const alertBox = document.getElementById('alert');
const alarmAudio = document.getElementById('alarmAudio');

const FPS = 6; // how many frames per second to send (reduce bandwidth)
let sending = true;

// get webcam
async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    video.srcObject = stream;
    await video.play();
    startSendingFrames();
  } catch (err) {
    alert('Unable to access camera: ' + err.message);
  }
}

function startSendingFrames() {
  const interval = 1000 / FPS;
  setInterval(() => {
    if (video.readyState < 2) return; // not ready
    // draw current frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    // reduce size for bandwidth
    canvas.toBlob((blob) => {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64data = reader.result; // data:image/jpeg;base64,...
        socket.emit('frame', base64data);
      };
      reader.readAsDataURL(blob);
    }, 'image/jpeg', 0.6);
  }, interval);
}

// socket listeners
socket.on('connect', () => {
  console.log('connected to server');
});

socket.on('ear', (data) => {
  if (data && data.ear !== undefined) {
    earVal.textContent = data.ear.toFixed(3);
  }
});

socket.on('no_face', () => {
  earVal.textContent = 'no face';
});

socket.on('drowsy', (data) => {
  console.log('Drowsy:', data);
  alertBox.style.display = 'block';
  // play alarm sound
  try {
    alarmAudio.currentTime = 0;
    alarmAudio.play();
  } catch (e) {
    console.warn('Audio play blocked:', e);
  }
  // Hide after a while
  setTimeout(() => { alertBox.style.display = 'none'; }, 3000);
});

// start
startCamera();
