let nextLevel = 'index.html';

const shoot = () => {
  const bullet = document.createElement("a-sphere");
  let pos = myCamera.getAttribute("position");
  bullet.setAttribute("position", pos);
  bullet.setAttribute("velocity", getDirection(myCamera, 30)); 
  bullet.setAttribute("dynamic-body", true);
  bullet.setAttribute("radius", 0.5);
  bullet.setAttribute("src", "https://i.imgur.com/H8e3Vnu.png");
  myScene.appendChild(bullet);
  bullet.addEventListener('collide', shootCollided); 
};

const teleport = () => {
  console.log('Pressing teleport...');
  const bullet = document.createElement("a-torus");
  let pos = myCamera.getAttribute("position");
  bullet.setAttribute("position", pos);
  bullet.setAttribute("velocity", getDirection(myCamera, 30));
  bullet.setAttribute("dynamic-body", true);
  bullet.setAttribute("radius", 0.5);
  bullet.setAttribute("arc", 360);
  bullet.setAttribute("radius-tubular", 0.1);
  bullet.setAttribute("rotation", { x: 90, y: 0, z: 0 });
  bullet.setAttribute("src", "https://i.imgur.com/H8e3Vnu.png");
  myScene.appendChild(bullet);
  bullet.addEventListener('collide', teleportCollided);
};

const shootCollided = event => {
  if (event.detail.body.el.id === 'floor') {
    console.log('Hit the floor'); 
    event.detail.target.el.removeEventListener('collide', shootCollided);
    myScene.removeChild(event.detail.target.el);
  } else if (event.detail.body.el.className === 'target') {
    console.log('Hit the target!');
    event.detail.target.el.removeEventListener('collide', shootCollided);
    myScene.removeChild(event.detail.target.el);
    myScene.removeChild(event.detail.body.el);
  }
  if (document.querySelectorAll('.target').length === 0) {
    console.log('You win!');
    //location.href = nextLevel;
  }
};

const teleportCollided = event => {
  if (event.detail.body.el.id === 'floor') {
    console.log('Hit the floor');
    event.detail.target.el.removeEventListener('collide', teleportCollided);
    let pos = event.detail.target.el.getAttribute('position');
    myScene.removeChild(event.detail.target.el);
    myCamera.setAttribute('position', { x: pos.x, y: 2, z: pos.z });
  }
};

document.onkeydown = event => {
  if (event.which == 32) {
    shoot();
  } else if (event.which == 67) {
    teleport();
  }
};
