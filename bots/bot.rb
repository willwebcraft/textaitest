require 'telegram_bot'
require 'dotenv'
require 'uri'
require 'net/http'

Dotenv.load('../.env')

token = ENV['BOT_TOKEN']
lambda = ENV['LAMBDA_URL']
bot = TelegramBot.new(token: token)

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
        else 
            reply.text = "What are you doing bro, #{command.inspect} means nothing at all."
        end
        puts "sending #{reply.text.inspect} to @#{message.from.username}"
        reply.send_with(bot)
    end
end

