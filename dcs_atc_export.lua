--[[
  DCS ATC Bot — weather export hook
  Place this file in:  %USERPROFILE%\Saved Games\DCS\Scripts\Hooks\

  BOT_HOST: IP address of the machine running the ATC bot.
    - If the bot is running on the SAME machine as DCS, set to "127.0.0.1"
    - If the bot is running on a DIFFERENT machine (e.g. dedicated server),
      set to that machine's local IP address (e.g. "192.168.1.50")
    - The bot machine must be reachable from the DCS server on BOT_PORT (UDP)

  BOT_PORT: must match DCS_EXPORT_PORT in the bot's .env (default 15099)
--]]

local BOT_HOST      = "192.168.1.32"
local BOT_PORT      = 15099
local INTERVAL_SEC  = 30
local LOG_FILE      = lfs.writedir() .. "Logs\\atc_export.log"  --luacheck: ignore

-- ---------------------------------------------------------------------------

local udp = nil
local socketOk, socketLib = pcall(require, "socket")
if socketOk then
    udp = socketLib.udp()
    udp:settimeout(0)
end

local function log(msg)
    local f = io.open(LOG_FILE, "a")
    if f then
        f:write(os.date("%H:%M:%S") .. " " .. msg .. "\n")
        f:close()
    end
end

local function send(payload)
    if udp then
        udp:sendto(payload, BOT_HOST, BOT_PORT)
    end
    log("SEND: " .. payload)
end


-- Map-origin query position, updated on mission load.
-- y = terrain height + 2m so the point is always above ground on any map.
local queryPosition = {x = 0, y = 100, z = 0}

local function updateQueryPosition()
    -- Try to resolve a sensible above-ground point at the map origin.
    -- land.getHeight is available in the hook environment and works on every map.
    local ok, h = pcall(land.getHeight, {x = 0, z = 0})  --luacheck: ignore land
    if ok and h and h >= 0 then
        queryPosition = {x = 0, y = h + 2, z = 0}
    else
        queryPosition = {x = 0, y = 100, z = 0}
    end
    log("queryPosition set: y=" .. tostring(queryPosition.y))
end

local function queryWeather()
    -- Weather singleton is available directly in the hook (GameGUI) environment.
    -- Returns live runtime values including dynamic weather — not static mission config.
    -- queryPosition is resolved at mission load so this works on any DCS map.
    local position = queryPosition

    local wind     = Weather.getGroundWindAtPoint({position = position})       --luacheck: ignore
    local temp_k, pressure_pa = Weather.getTemperatureAndPressureAtPoint({     --luacheck: ignore
        position = position
    })

    -- wind.v = speed m/s, wind.a = direction FROM in degrees true
    -- temp_k is already in Celsius (despite the name; DCS returns C not K here)
    local wind_speed   = wind.v
    local wind_dir     = wind.a
    local temp_c       = temp_k
    local pressure_hpa = pressure_pa / 100.0

    return string.format(
        '{"wind_dir":%g,"wind_speed_ms":%g,"pressure_hpa":%g,"temp_c":%g}',
        wind_dir, wind_speed, pressure_hpa, temp_c
    )
end

local lastSent  = 0
local callbacks = {}

function callbacks.onMissionLoadEnd()
    log("onMissionLoadEnd fired. socket=" .. tostring(socketOk))
    updateQueryPosition()
    send('{"status":"hook_alive"}')
    lastSent = 0
end

function callbacks.onSimulationFrame()
    local now = os.time()
    if now - lastSent < INTERVAL_SEC then return end
    lastSent = now

    local ok, result = pcall(queryWeather)
    if ok and result and result ~= "" and result ~= "nil" then
        send(result)
    else
        local err = ok and "empty result" or tostring(result)
        send('{"error":"' .. err .. '"}')
    end
end

log("Script loaded. socket=" .. tostring(socketOk))
DCS.setUserCallbacks(callbacks)  --luacheck: ignore
