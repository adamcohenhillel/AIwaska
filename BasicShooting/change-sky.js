AFRAME.registerComponent('school-playground', {
    init: function () {
      const myTimeout = setTimeout(myGreeting, 10000);

      function myGreeting(){
        console.log("wait!")
      }
      // Solution for Modifying Entities.
      var sceneEl = document.querySelector('a-scene'); 
      var backgroundImages = [            
            'https://cdn.aframe.io/360-image-gallery-boilerplate/img/city.jpg',
            'https://iili.io/HnQTbpe.png',
            'https://iili.io/HnQTDv9.png',
            'https://iili.io/HnQTpTu.png',
            'https://iili.io/HnQJjsa.png',
            'https://iili.io/HnLr7bS.png',
            'https://iili.io/HnQTyhb.png',
            'https://iili.io/HnL4R4a.png'

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

  