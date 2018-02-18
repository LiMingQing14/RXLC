local add = require "add"
local sub = require "sub"

local function main()
	local result = add(1, 2)
	print(result)

    result = sub(2, 1)
    print(result)
end

main()