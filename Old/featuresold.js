document.addEventListener("DOMContentLoaded", function() {
    var btn = document.querySelector('.btn');
    var box = document.querySelector('.box');
  
    btn.addEventListener('click', function() {
      this.classList.toggle('active');
      box.classList.toggle('open');
    });
  });
  