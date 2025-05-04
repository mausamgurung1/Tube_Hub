// Basic example: Toggle like button color on click
document.querySelectorAll('.like-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('liked');
      btn.style.fill = btn.classList.contains('liked') ? 'red' : 'none';
    });
  });
  