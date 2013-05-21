javaaddpath(['utils/httpcomponents-core-4.2.4/lib/httpcore-4.2.4.jar']);
javaaddpath(['utils/httpcomponents-client-4.2.5/lib/httpclient-4.2.5.jar']);

% import org.apache.http.impl.client.DefaultHttpClient;
% import org.apache.http.client.methods.HttpPost;
% import org.apache.http.entity.StringEntity;

import org.apache.http.impl.client.*;
import org.apache.http.client.methods.*;
import org.apache.http.entity.*;

% clear all;
% close all;
% clc;

% Library stuff
addpath('jsonlab/');
addpath('features/');

% Global stuff
tickers = {};
global_results = {};
items = dir('stock_data');

for index = 1:length(items)
    item = items(index);
    if ~item.isdir
        ticker_json = regexp(item.name, '\w+', 'match');
        tickers{length(tickers)+1} = ticker_json(1);
    end
end

% Market data
disp('Loading market data');
file_path = strcat('stock_data/^GSPC.json');
disp('.');
markets = loadjson(file_path);
markets_date = [];
for i = {markets.date}
    markets_date = [ markets_date datenum(i{:}, 'yyyy-mm-dd')];
end
markets_date = fliplr(markets_date');
markets_close = [];
for i = {markets.price_close}
    markets_close = [ markets_close i{:}];
end
markets_close = fliplr(markets_close');
markets_high = [];
for i = {markets.price_high}
    markets_high = [ markets_high i{:}];
end
markets_high = fliplr(markets_high');
markets_low = [];
for i = {markets.price_low}
    markets_low = [ markets_low i{:}];
end
markets_low = fliplr(markets_low');

% Load betas
disp('Loading beta data');
betas = loadjson('betas.json');
disp('.');


% for cc = 1:length(tickers)
for cc = 9
    beta_value = 0;

    ticker = tickers{cc}

    % Search for beta
    for b=1:length(betas)
        ticker_1 = ticker{:};
        ticker_2 = betas(b).ticker;
        if strcmp(ticker_1, ticker_2) == 1
            beta_value = betas(b).beta
        end
    end
    disp(['Beta ', num2str(beta_value) ])

    % Ticket
    % ticket = 'USB';
    % stocks = hist_stock_data('01012008', '01012013', ticket);
    file_path = strcat('stock_data/', ticker, '.json');
    if exist(file_path{:}, 'file')
        stocks_load;
        targets_load;
        if length(targets) > 1
            % accuracy;
            % proximity;
            % profitability;
            % reach_time;
            impact_to_market;
            % aggressiveness; % OK
        else
            disp('No target data found');
        end
    else
        disp('No stock data found');
    end

    % Making random variables to set the TP
    % Three banks
    % banks = 1:3;
    % banks = 1;  % one bank
    % Colors for the banks
    % colors = ['r', 'g', 'b'];

    

    %% Epsillon

    % clear bank;
    % for bank = banks
    %   
    %   Epsillon_s = [];
    %   Epsillon_l = [];
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    % 
    % 	for i = 1:length(bank_dates)
    %     
    %     epsillon_l = 0;
    %     epsillon_l_index = 0;
    %     epsillon_s = 0;
    %     epsillon_s_index = 0;
    %     
    %     bank_date = bank_dates(i);
    %     bank_price = bank_prices(i);
    % 
    % 		start_index = find(stocks_date==bank_date);
    % 		end_index = start_index + 250;
    %     if end_index > length(stocks_date)
    %       end_index = length(stocks_date) - 1;
    %     end
    %    
    % 		till_bank_date = stocks_date(end_index);
    %     
    %     end_index = find(stocks_date==till_bank_date);
    %     
    %     for j = start_index:end_index
    %     
    %       if bank_price > stocks_close(start_index)
    %         ep = ( stocks_high(j) - stocks_close(start_index) ) / stocks_close(start_index);
    %         
    %         if ep > epsillon_l
    %           epsillon_l = ep;
    %           epsillon_l_index = j;
    %         end
    %         epsillon_s = 0;
    %         
    %       else
    %         epsillon_l = 0;
    %         ep = ( stocks_close(start_index) - stocks_low(j) ) / stocks_close(start_index);
    %         
    %         if ep > epsillon_s
    %           epsillon_s = ep;
    %           epsillon_s_index = j;
    %         end
    %         
    %       end
    %       
    %     end
    %     
    %     if epsillon_l_index ~= 0
    %       hold all;
    %       plot([stocks_date(start_index) stocks_date(epsillon_l_index) ], [stocks_high(start_index) stocks_high(epsillon_l_index) ], ... 
    %         '-.', 'Color', colors(bank), 'LineWidth', 3);
    %       hold off;
    %     end
    %     
    %     if epsillon_s_index ~= 0
    %       hold all;
    %       plot([stocks_date(start_index) stocks_date(epsillon_s_index) ], [stocks_high(start_index) stocks_high(epsillon_s_index) ], ... 
    %         '-.', 'Color', colors(bank), 'LineWidth', 3);
    %       hold off;
    %     end
    % 
    %     Epsillon_l(end+1) = epsillon_l;
    %     Epsillon_s(end+1) = epsillon_s;
    % 
    %   end
    %   
    %   Epsillon_total = [ Epsillon_l Epsillon_s ];
    %   
    %   disp('Bankas');
    %   disp(colors(bank));
    %   disp('Long');
    %   disp(Epsillon_l);
    %   disp(sum(Epsillon_l)/length(find(Epsillon_l~=0)));
    %   disp('Short');
    %   disp(Epsillon_s);
    %   disp(sum(Epsillon_s)/length(find(Epsillon_s~=0)));
    %   disp('Total');
    %   disp(sum(Epsillon_total)/length(find(Epsillon_total~=0)));
    % 
    % end


    %% Eta

    % clear bank;
    % for bank = banks
    %   
    %   beta_e = 0.10;
    %   
    %   Eta = [];
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    %   
    %   bank_dates = sort(bank_dates);
    %   
    %   disp(bank_dates);
    %   
    %   eta = diff(bank_dates);
    %   
    %   disp(eta);
    %   
    %   eta = eta(eta<250);
    %   
    %   disp(eta);
    %   
    %   disp('Bankas');
    %   disp(colors(bank));
    %   disp(Eta);
    % 
    % end

    %% Theta

    % clear bank;
    % for bank = banks
    %   
    %   disp('Bankas');
    %   disp(colors(bank));
    %   
    %   Theta = [];
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    %   
    %   disp('Bank prices');
    %   theta_raw = sign(diff(bank_prices));
    %   
    %   disp(diff(bank_prices));
    %   
    %   theta = 0;
    %   
    %   for j=1:length(theta_raw)-1;
    %     
    %     current_theta = theta_raw(j);
    %     future_theta = theta_raw(j+1);
    %     
    %     if current_theta ~= future_theta
    %       theta = theta - 1;
    %     end
    %     
    %   end
    %   
    %   disp(bank_prices);
    %   disp(theta);
    % 
    % end

    %% iota

    % Lets calculate the consensus

    % clear bank;
    % Consensus = zeros(length(banks), length(stocks_date));
    % for bank = banks
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    % 
    % 	for i = 1:length(bank_dates)
    %     
    %     bank_date = bank_dates(i);
    %     bank_price = bank_prices(i);
    % 
    % 		start_index = find(stocks_date==bank_date);
    % 		end_index = start_index + 250;
    %     
    %     if end_index > length(stocks_date)
    %       end_index = length(stocks_date) - 1;
    %     end
    %    
    % 		till_bank_date = stocks_date(end_index);
    %     
    %     end_index = find(stocks_date==till_bank_date);
    %     
    %     Consensus(bank,start_index:end_index) = bank_price;
    % 
    %   end
    % 
    % end
    % 
    % % Sum over the dates
    % vector_cons = [];
    % for i=1:length(stocks_date)
    %   
    %   if i > 90
    %     current_cons = sum(Consensus(i-90:i))/sum(Consensus(i-90:i)~=0);
    %     vector_cons(end+1) = current_cons;
    %   else
    %     vector_cons(end+1) = 0;
    %   end
    %   
    % end
    % 
    % hold all;
    % plot(stocks_date, vector_cons);
    % hold off;
    % 
    % clear bank;
    % for bank = banks
    %   
    %   Iota = [];
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    % 
    % 	for i = 1:length(bank_dates)
    %     
    %     bank_date = bank_dates(i);
    %     bank_price = bank_prices(i);
    % 
    % 		start_index = find(stocks_date==bank_date);
    % 		end_index = start_index + 250;
    %     
    %     if end_index > length(stocks_date)
    %       end_index = length(stocks_date) - 1;
    %     end
    %    
    % 		till_bank_date = stocks_date(end_index);
    %     
    %     end_index = find(stocks_date==till_bank_date);
    %     if start_index > 90
    %       m_con = sum(Consensus(start_index-90:start_index))/sum(Consensus(start_index-90:start_index)~=0);
    %     
    %       iota = (bank_price - m_con)/m_con;
    %     else
    %       iota = 0;
    %     end
    %     disp(colors(bank));
    %     disp(iota);
    %     
    %     Iota(end+1) = iota;
    % 
    %   end
    %   
    %   disp('Iota');
    %   disp(sum(Iota)/3);
    % 
    % end

    clear i;

    for i=1:length(global_results)
        httpclient = DefaultHttpClient();
        httppost = HttpPost('http://localhost:8000/api/check/');
        httppost.addHeader('Content-Type', 'application/json');
        httppost.addHeader('Accept', 'application/json');
        data = savejson('', global_results{i});
        params = StringEntity(data);
        httppost.setEntity(params);

        response = httpclient.execute(httppost);
        disp(response);
    end
end