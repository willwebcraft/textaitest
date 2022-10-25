require 'telegram_bot'
require 'dotenv'
require 'uri'
require 'net/http'

Dotenv.load('../../.env')

token = ENV['BOT_TOKEN']
lambda = ENV['LAMBDA_URL']
bot = TelegramBot.new(token: token)
python_script = '../../auto.py'
intro_text = "Hello, use the commands !"

bot.get_updates(fail_silently: true) do |message|
    puts "@#{message.from.username}: #{message.text}"
    command = message.get_command_for(bot)

    message.reply do |reply|
        case command
        when /start/i
            reply.text = "Hello World !"
        when /greet/i
            reply.text = "Hello #{message.from.first_name} !"
        when /lambda/i
            uri = URI(lambda)
            res = Net::HTTP.get_response(uri)
            reply.text = "END"
            puts res.body if res.is_a?(Net::HTTPSuccess)
        when /text_commands/i
            reply.text = "Waiting for the result, please be patient bitch !"
            #result = exec('python ' + python_script)
            output = `python #{python_script}`
            reply.text = intro_text
        else 
            reply.text = "What are you doing bro, #{command.inspect} means nothing at all."
        end
        puts "sending #{reply.text.inspect} to @#{message.from.username}"
        reply.send_with(bot)
    end
end

