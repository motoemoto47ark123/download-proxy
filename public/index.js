const downloadButton = document.querySelector('button[type="submit"]');

downloadButton.addEventListener('mouseover', () => {
  downloadButton.style.backgroundColor = 'darkred';
});

downloadButton.addEventListener('mouseout', () => {
  downloadButton.style.backgroundColor = 'red';
});
