AFRAME.registerComponent('school-playground', {
    init: function () {
      // Solution for Modifying Entities.
      var sceneEl = document.querySelector('a-scene'); 
      var backgroundImages = [
            'https://i.imgur.com/mYmmbrp.jpg',
            'https://cdn.aframe.io/360-image-gallery-boilerplate/img/city.jpg'
        ];
        setInterval(changeBackground, 3000);                                
        let currentBackgroundIndex = 0;
      
        function changeBackground() {
          sceneEl.querySelector('a-sky').setAttribute('src', backgroundImages[currentBackgroundIndex]);  
          currentBackgroundIndex++;
          if (currentBackgroundIndex >= backgroundImages.length) {
                currentBackgroundIndex = 0;
            }                
          }
    }
  });

