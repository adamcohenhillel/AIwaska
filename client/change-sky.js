AFRAME.registerComponent('school-playground', {
    init: function () {
      // Solution for Modifying Entities.
      var sceneEl = document.querySelector('a-scene');
        let fileNumber = 1
        let go_up = true;
        function changeBackground() {
          let filePath = "assets/" + fileNumber + ".png"
          sceneEl.querySelector('a-sky').setAttribute('src', filePath);
          if (go_up) {
            fileNumber++;
          }
          else{
            fileNumber--;
          }

          if (fileNumber == 113) {
            go_up = false;
          }
          else if (fileNumber == 0) {
            go_up = true;
          }
      }
      setInterval(changeBackground, 100);
    }
  });

  