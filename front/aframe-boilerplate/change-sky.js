AFRAME.registerComponent('school-playground', {
    init: function () {
      
      // Solution for Modifying Entities.
      var sceneEl = document.querySelector('a-scene'); 
      var backgroundImages = [                    
          "assets/1.jpg",
           "assets/2.jpg",
           "assets/3.jpg"
         ];           
        setInterval(changeBackground, 3000);                                
        let currentBackgroundIndex = 0;
      
        function changeBackground() {
          sceneEl.querySelector('a-sky').setAttribute('src', backgroundImages[currentBackgroundIndex]);  
          console.log("ttt")
          currentBackgroundIndex++;
          if (currentBackgroundIndex >= backgroundImages.length) {
                currentBackgroundIndex = 0;
            }                
          }
    }
  });

  