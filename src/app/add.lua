local function add(...)
    local ret = 0
    for _, v in ipairs({...}) do
        ret = ret + v
    end
    return ret
end

return add