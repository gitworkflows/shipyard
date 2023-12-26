'use strict';

async function handler() {
  return 'Hi Shipyard';
}

module.exports = {
  createUserHandler: handler,
  authenticateUserHandler: handler
};
