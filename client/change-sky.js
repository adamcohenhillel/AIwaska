AFRAME.registerComponent('school-playground', {
    init: function () {
      
      // Solution for Modifying Entities.
      var sceneEl = document.querySelector('a-scene');       
        setInterval(changeBackground, 3000);                                
        let fileNumber = 1;      
        function changeBackground() {
          let filePath = "assets/" + fileNumber + ".jpg"          
          sceneEl.querySelector('a-sky').setAttribute('src', filePath);  
          while(fileNumber = 3) {
            fileNumber = 1;
          }          
      }
    }
  });

  