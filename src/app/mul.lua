local function mul(a, ...)
    local ret = a
    for _, v in ipairs({...}) do
        ret = ret * v
    end
    return ret
end

return mul