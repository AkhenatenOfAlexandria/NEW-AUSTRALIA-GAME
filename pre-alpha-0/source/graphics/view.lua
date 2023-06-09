local view = {}

local scale = function (self)
  return love.graphics.getWidth() / self.gameWidth
end

local clamp = function (min, n, max)
  if n < min then return min end
  if n > max then return max end
  return n
end

local viewOffset = 10

local update = function (self, game)
  local currentRoom = game.map:currentRoom()
  local maxX = (currentRoom.roomWidth - self.gameWidth) + viewOffset
  local maxY = (currentRoom.roomHeight - self.gameHeight) + viewOffset
  self.x = clamp(-viewOffset, game.player.drawX - self.gameWidth / 2, maxX)
  self.z = clamp(-viewOffset, game.player.drawY - self.gameHeight / 2, maxY)
end

local inContext = function (self, drawFunction)
  local scale = scale(self)
  love.graphics.push('all')
  love.graphics.scale(scale, scale)
  love.graphics.translate(-self.x, -self.z)
  drawFunction()
  love.graphics.pop()
end

view.create = function (gameWidth, gameHeight, x, y)
  local instance = {}

  instance.gameWidth = gameWidth
  instance.gameHeight = gameHeight
  instance.x = x
  instance.y = y

  instance.inContext = inContext
  instance.update = update

  return instance
end

return view