local add = require "add"
local sub = require "sub"
local mul = require "mul"
local div = require "div"

local function main()
    local result = add(8, 4, 2, 1)
    print("add(8, 4, 2, 1) = " + result)

    result = sub(8, 4, 2, 1)
    print("sub(8, 4, 2, 1) = " + result)

    result = mul(8, 4, 2, 1)
    print("mul(8, 4, 2, 1) = " + result)

    result = div(8, 4, 2, 1)
    print("div(8, 4, 2, 1) = " + result)
end

main()