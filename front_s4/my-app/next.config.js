const path = require('path');

module.exports = {
  // ... outras configurações ...
  async rewrites() {
    return [
      { 
        source: '/index',  
        destination: '/pages/index.jsx',
      },
      { 
        source: '/planes',  
        destination: '/pages/planes.jsx',
      },
      { 
        source: '/upload',  
        destination: '/pages/upload.jsx',
      },
      { 
        source: '/signout',  
        destination: '/pages/signout.jsx',
      },
    ];
  },
};

