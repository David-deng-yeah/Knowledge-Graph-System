-- read_query() gets the client query before it reaches the server
-- @param packet : the mysql-packet sent by client
--
-- the packet contains a command-packet:
--  * the first byte the type (e.g. proxy.COM_QUERY)
--  * the argument of the command
--
--   http://forge.mysql.com/wiki/MySQL_Internals_ClientServer_Protocol#Command_Packet
-- for a COM_QUERY it is the query itself in plain-text
function read_query( packet )
    local _com = string.byte(packet)
    local _sql = string.sub(packet,2)
	if string.byte(packet) == proxy.COM_QUERY then
        --
    else
        print "X"
	end
    print(_sql)
end

local password = assert(require("mysql.password"))
local proto = assert(require("mysql.proto"))

local new_user = "app_gbase_zhjj"
local new_password = "drawer@#$0427"

-- .on auth
function read_auth()
	local c = proxy.connection.client
	local s = proxy.connection.server

    -- learn from baidu
    local protocol_41_default_capabilities = 8+512+32768

    -- debug
	-- print(("for challenge %q the client sent %q"):format(
	-- 	s.scramble_buffer,
	-- 	c.scrambled_password
	-- ))

--	-- if we know this user, replace its credentials
--	local mapped = map_auth[c.username]
--    print(c.username)
--	if mapped and
--		password.check(
--			s.scramble_buffer,
--			c.scrambled_password,
--			password.hash(password.hash(mapped.password))
--		) then
--
		proxy.queries:append(1,
			proto.to_response_packet({
				-- username = mapped.new_user,
				username = new_user,
				-- response = password.scramble(s.scramble_buffer, password.hash(mapped.new_password)),
				response = password.scramble(s.scramble_buffer, password.hash(new_password)),
                server_capabilities = protocol_41_default_capabilities, -- learn from baidu
				charset  = 8, -- default charset
				database = c.default_db,
				max_packet_size = 1 * 1024 * 1024
			})
		)

		return proxy.PROXY_SEND_QUERY
--	end

end -- read_auth()

