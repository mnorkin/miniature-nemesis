clear all;
close all;
clc;

addpath('jsonlab/');

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

% for cc = 1:length(tickers)
for cc = 9

    ticker = tickers{cc}

    % Ticket
    % ticket = 'USB';
    % stocks = hist_stock_data('01012008', '01012013', ticket);
    file_path = strcat('stock_data/', ticker, '.json');
    stocks = loadjson(file_path{:});
    % load stocks;

    % Organize dates
    stocks_date = [];
    for i = {stocks.date}
        stocks_date = [ stocks_date datenum(i{:}, 'yyyy-mm-dd') ]; %#ok<AGROW>
    end
    stocks_date = fliplr(stocks_date');

    stocks_close = [];
    for i = {stocks.price_close}
      stocks_close = [ stocks_close i{:} ];
    end
    stocks_close = fliplr(stocks_close');

    % stocks_date = stocks_date - 7.334e5;

    % Organize high
    stocks_high = [];
    for i = {stocks.price_high}
        stocks_high = [ stocks_high i{:} ]; %#ok<AGROW>
    end
    stocks_high = fliplr(stocks_high');

    % Organize low
    stocks_low = [];
    for i = { stocks.price_low }
        stocks_low = [ stocks_low i{:} ]; %#ok<AGROW>
    end
    stocks_low = fliplr(stocks_low');

    % Calculate stock delta from high
    stocks_delta = [];
    for i = 2:length(stocks_high)
      stocks_delta = [ stocks_delta (stocks_high(i) - stocks_high(i-1))/stocks_high(i-1) ]; %#ok<AGROW>
    end
    % stocks_delta = fliplr(stocks_delta');

    % Plot the data
    figure(1);
    clf;
    hold all;
    % plot(stocks_date, stocks_low, 'm-');
    plot(stocks_date, stocks_high, 'm-');
    % plot(stocks_date, stocks_close, 'm-');
    hold off;

    grid on;
    xlabel('Date');
    ylabel('Price, normalized');
    datetick('x', 'yyyy-mm-dd');

    % Making random variables to set the TP
    % Three banks
    % banks = 1:3;
    % banks = 1;  % one bank
    % Colors for the banks
    % colors = ['r', 'g', 'b'];

    % Loading the data
    % load dates;
    % load prices;
    file_path = strcat('target_data/', ticker, '.json');
    targets = loadjson(file_path{:});

    banks = unique({targets(:).analytic});

    % Sorting mechanism
    clear bank;
    for bank = 1:length(banks)

        bank_dates = [];
        bank_prices = [];

        bank_name = banks(bank);

        disp(['Searching for ' bank_name{:} ])

        entries = strfind({targets(:).analytic}, bank_name{:});

        for index = 1:length(entries)
            entry = entries(index);
            if length(entry{:}) > 0
                disp(targets(index));
                bd = datenum(targets(index).date_human, 'yyyy-mm-dd');
                if addtodate(bd, 1, 'year') < now
                    bank_dates(length(bank_dates)+1) = datenum(targets(index).date_human, 'yyyy-mm-dd');
                    bank_prices(length(bank_prices)+1) = targets(index).price;
                end
            end
        end
      
        % for i = 1:length(bank_dates)-1

        %     current_bank_date = bank_dates(i,:);
        %     future_bank_date = bank_dates(i+1);

        %     if current_bank_date > future_bank_date
        %         current_bank_price = bank_prices(i);
        %         future_bank_price = bank_prices(i+1);

        %         bank_dates(i) = future_bank_date;
        %         bank_dates(i+1) = current_bank_date;

        %         bank_prices(i) = future_bank_price;
        %         bank_prices(i+1) = current_bank_price;

        %     end

        % end

        dates(bank) = {bank_dates'};
        prices(bank) = {bank_prices'};
      
    end

    clear bank;
    for bank = 1:length(banks)
      
    	bank_dates = dates{bank};
    	bank_prices = prices{bank};
      
    	for i = 1:length(bank_dates)

    		bank_date = bank_dates(i);
    		bank_price = bank_prices(i);

    		start_index = find(stocks_date==bank_date);
    		end_index = start_index + 250;
    		if end_index > length(stocks_date)
    				end_index = length(stocks_date);
    		end
    		till_bank_date = stocks_date(end_index);
        
    %     for check_bank_date=bank_dates
    %       if check_bank_date ~= bank_date
    %         if bank_date < check_bank_date && till_bank_date > check_bank_date
    %           till_bank_date = check_bank_date;
    %         end
    %       end
    %     end

    		hold all;
    % 		plot([bank_date till_bank_date], [bank_price bank_price], 'Color', colors(bank));
    % 		plot([bank_date till_bank_date], [bank_price bank_price], 'x', 'LineWidth', 6, 'Color', colors(bank));
            plot(bank_date, bank_price, 'x', 'LineWidth', 6);
    		hold off;

    		% for j=start_index:40:end_index
    			% hold all;
    % 			line([stocks_date(j), stocks_date(j)], [stocks_high(j) bank_price], 'Color', colors(bank));
    			% hold off;
    		% end

    	end
        get(0,'DefaultAxesColorOrder');
    end

    %% Alpha 
    disp('Alpha');
    disp('Accuracy')

    clear bank;
    for bank = 1:length(banks)
    % for bank = 60
      
        Alpha = [];
    
    	bank_dates = dates(bank);
        if iscell(bank_dates)
            bank_dates = bank_dates{:};
        end

    	bank_prices = prices(bank);

        if iscell(bank_prices)
            bank_prices = bank_prices{:};
        end
    
    	for i = 1:length(bank_dates)
        
            bank_date = bank_dates(i);

    		start_index = find(stocks_date==bank_date);
    		end_index = start_index + 250;

    		
            if end_index > length(stocks_date)
    			end_index = length(stocks_date);
            end
       
    		till_bank_date = stocks_date(end_index);
        
            for check_bank_date=bank_dates
                if check_bank_date ~= bank_date
                    if bank_date < check_bank_date && till_bank_date > check_bank_date
                        till_bank_date = check_bank_date;
                    end
                end
            end
        
            end_index = find(stocks_date==till_bank_date);
    
    		alpha = 0;
    
    		bank_price = bank_prices(i);
    
    		clear j;
    
    		for j=start_index:end_index-1
    
    			if alpha == 0 && bank_price < stocks_high(j) && bank_price > stocks_high(j+1)
    				hold all;
    				plot(stocks_date(j), bank_price, 'x', 'LineWidth', 8);
    				hold off;
                    alpha = 1;
    			end
    
    			if alpha == 0 && bank_price < stocks_low(j) && bank_price > stocks_low(j+1)
    				hold all;
    				plot(stocks_date(j), bank_price, 'x', 'LineWidth', 8);
    				hold off;
                    alpha = 1;
    			end
    
    			if alpha == 0 && bank_price > stocks_high(j) && bank_price < stocks_high(j+1)
    				hold all;
    				plot(stocks_date(j), bank_price, 'x', 'LineWidth', 8);
    				hold off;
                    alpha = 1;
                end
    
    			if alpha == 0 && bank_price > stocks_low(j) && bank_price < stocks_low(j+1)
    				hold all;
    				plot(stocks_date(j), bank_price, 'x', 'LineWidth', 8);
    				hold off;
                    alpha = 1;
                end
          
            end
        
            Alpha = [Alpha alpha];
    
        end
      
          disp('Bankas');
          disp(banks(bank));
          disp(sum(Alpha)/length(bank_prices));
          result = sum(Alpha)/length(bank_prices)*100.00;
          if isnan(result)
            result = 0
          end
          result = round(result*100)/100
          global_results{length(global_results)+1} = struct( ...
            'feature', 'accuracy', ...
            'analytic', banks(bank), ...
            'ticker', ticker, ...
            'value', result ...
          );
    
    end


    %% Beta
 %    disp('Beta');
 %    disp('Proximity')

 %    clear bank;
 %    for bank = 1:length(banks)
      
 %    Beta = [];

 %    bank_dates = dates(bank);
 %    if iscell(bank_dates)
 %        bank_dates = bank_dates{:};
 %    end
 %    bank_prices = prices(bank);
 %    if iscell(bank_prices)
 %        bank_prices = bank_prices{:};
 %    end

	% for i = 1:length(bank_dates)
        
 %        bank_date = bank_dates(i);
	% 	start_index = find(stocks_date==bank_date);
	% 	end_index = start_index + 249;
	% 	if end_index > length(stocks_date)-1
	% 		end_index = length(stocks_date);
 %        end
       
	% 	till_bank_date = stocks_date(end_index);
        
 %        for ii=1:length(bank_dates)
 %            check_bank_date = bank_dates(ii);
 %            if check_bank_date ~= bank_date
 %                if bank_date < check_bank_date && till_bank_date > check_bank_date
 %                      till_bank_date = check_bank_date;
 %                end
 %            end
 %        end
        
 %        end_index = find(stocks_date==till_bank_date);

	% 	beta = 0;

	% 	bank_price = bank_prices(i);

	% 	clear j;

	% 	for j=start_index:end_index-1
 %            if (stocks_high(j) > bank_price) && (stocks_low(j) > bank_price)
 %        		beta = beta + abs( stocks_high(j) - bank_price )/length(start_index:end_index);
 %            elseif (stocks_low(j) < bank_price) && (stocks_high(j) < bank_price)
 %                beta = beta + abs( stocks_low(j) - bank_price )/length(start_index:end_index);
 %            end
 %        end
        
 %        Beta = [Beta beta];

 %        end

 %        disp('Bankas');
 %        disp(banks(bank));
 %        % disp(Beta);
 %        disp(sum(Beta)/length(bank_prices));
 %        result = sum(Beta)/length(bank_prices);

 %        global_results{length(global_results)+1} = struct( ...
 %            'feature', 'proximity', ...
 %            'analytic', banks(bank), ...
 %            'ticker', ticker, ...
 %            'value', result ...
 %          );

 %    end

    %% Gamma

    % clear bank;
    % for bank = banks
    %   
    %   Gamma = [];
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    % 
    % 	for i = 1:length(bank_dates)
    %     
    %     bank_date = bank_dates(i);
    % 
    % 		start_index = find(stocks_date==bank_date);
    % 		end_index = start_index + 250;
    % 		if end_index > length(stocks_date)
    % 				end_index = length(stocks_date);
    %     end
    %    
    % 		till_bank_date = stocks_date(end_index);
    %     
    % %     for check_bank_date=bank_dates
    % %       if check_bank_date ~= bank_date
    % %         if bank_date < check_bank_date && till_bank_date > check_bank_date
    % %           till_bank_date = check_bank_date;
    % %         end
    % %       end
    % %     end
    %     
    %     end_index = find(stocks_date==till_bank_date);
    % 
    % 		gamma = 0;
    % 
    % 		bank_price = bank_prices(i);
    % 
    % 		clear j;
    % 
    % 		for j=start_index:end_index-1
    % 
    % 			if gamma == 0 && bank_price < stocks_high(j) && bank_price > stocks_high(j+1)
    % 				hold all;
    % 				plot(stocks_date(j), bank_price, 'x', 'Color', colors(bank), 'LineWidth', 8);
    % 				hold off;
    %         gamma = j - start_index;
    % 			end
    % 
    % 			if gamma == 0 && bank_price < stocks_low(j) && bank_price > stocks_low(j+1)
    % 				hold all;
    % 				plot(stocks_date(j), bank_price, 'x', 'Color', colors(bank), 'LineWidth', 8);
    % 				hold off;
    %         gamma = j - start_index;
    % 			end
    % 
    % 			if gamma == 0 && bank_price > stocks_high(j) && bank_price < stocks_high(j+1)
    % 				hold all;
    % 				plot(stocks_date(j), bank_price, 'x', 'Color', colors(bank), 'LineWidth', 8);
    % 				hold off;
    %         gamma = j - start_index;
    %       end
    % 
    % 			if gamma == 0 && bank_price > stocks_low(j) && bank_price < stocks_low(j+1)
    % 				hold all;
    % 				plot(stocks_date(j), bank_price, 'x', 'Color', colors(bank), 'LineWidth', 8);
    % 				hold off;
    %         gamma = j - start_index;
    %       end
    %       
    %     end
    %     
    %     if gamma == 0
    % %       gamma = length(start_index:end_index);
    %     end
    %     
    %     Gamma = [Gamma gamma];
    % 
    %   end
    %   
    %   disp('Bankas');
    %   disp(colors(bank));
    %   disp(Gamma);
    %   disp(sum(Gamma)/length(find(Gamma~=0)));
    % 
    % end

    %% Delta

    % clear bank;
    % for bank = 1:1
    %   
    %   disp('Bankas');
    %   disp(colors(bank));
    %   
    %   Delta_l = [];
    %   Delta_s = [];
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    % 
    % 	for i = 1:length(bank_dates)
    %     
    %     delta_l = 0;
    %     delta_s = 0;
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
    %     if stocks_close(start_index) < bank_price
    %       delta_l = ( stocks_close(end_index+1) - stocks_close(start_index) ) / stocks_close(start_index);
    %       delta_s = 0;
    %       disp('Delta l');
    %       disp([num2str(stocks_close(end_index+1)) ' ' num2str(stocks_close(start_index)) ' ' num2str(delta_l)]);
    %     else
    %       delta_l = 0;
    %       delta_s = ( stocks_close(start_index) - stocks_close(end_index+1) ) / stocks_close(start_index);
    %       disp('Delta s');
    %       disp([num2str(stocks_close(end_index+1)) ' ' num2str(stocks_close(start_index)) ' ' num2str(delta_s)]);
    %     end
    %     
    %     hold all;
    %     plot([stocks_date(start_index) stocks_date(end_index) ], [stocks_close(start_index) stocks_close(end_index+1) ], ... 
    %       '-.', 'Color', colors(bank), 'LineWidth', 3);
    %     hold off;
    %     
    %     Delta_l(end+1) = delta_l;
    %     Delta_s(end+1) = delta_s;
    % 
    %   end
    %   
    %   Delta_total = [ Delta_l Delta_s ];
    %   
    %   disp('Long');
    %   disp(Delta_l);
    %   disp('Short');
    %   disp(Delta_s);
    %   
    %   disp('Long');
    %   disp(sum(Delta_l)/length(find(Delta_l~=0)));
    %   disp('Short');
    %   disp(sum(Delta_s)/length(find(Delta_s~=0)));
    %   
    %   disp('Total');
    %   disp(sum(Delta_total)/length(find(Delta_total~=0)));
    % 
    % end

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

    %% Zeta

    % A little help for the construction of market
    % market_index = sin((1:length(stocks_date))/(20*pi))/10+0.5;
    % 
    % bbeta_e = [ 1.0 1.1 0.9 ] ;
    % 
    % 
    % 
    % clear bank;
    % 
    % for beta_e = bbeta_e
    %   fprintf('Beta: %f\n', beta_e);
    %   fprintf('Zeta_p\tZeta_m\tZeta\n');
    %   
    %   for bank = banks
    % 
    %     fprintf('Bankas: %s\n', colors(bank));
    %   %   disp(colors(bank));
    % 
    % 
    % 
    %     Zeta = [];
    % 
    %     bank_dates = dates(bank,:);
    %     bank_prices = prices(bank,:);
    % 
    %     for i = 1:length(bank_dates)
    % 
    %       zeta_m = 0;
    %       zeta_p = 0;
    % 
    %       bank_date = bank_dates(i);
    %       bank_price = bank_prices(i);
    % 
    %       start_index = find(stocks_date==bank_date);
    %       end_index = start_index + 250;
    %       if end_index > length(stocks_date)
    %         end_index = length(stocks_date) - 1;
    %       end
    % 
    %       till_bank_date = stocks_date(end_index);
    % 
    %       end_index = find(stocks_date==till_bank_date);
    % 
    %       for j = start_index:start_index+1
    % 
    %         zeta_p = zeta_p + (stocks_close(start_index) - stocks_close(j))/stocks_close(start_index);
    % 
    %       end
    % 
    %       for j = start_index:start_index+1
    % 
    %         zeta_m = zeta_m + (market_index(start_index) - market_index(j))/market_index(start_index);
    % 
    %       end
    % 
    %       zeta_p = zeta_p/length(start_index:start_index+1);
    % 
    %   %     fprintf('Zeta p: %f\n', zeta_p);
    %   %     disp(zeta_p);
    % 
    %       zeta_m = zeta_m/length(start_index:start_index+1);
    % 
    %   %     fprintf('Zeta m: %f\n', zeta_m);
    %   %     disp(zeta_m);
    % 
    %       % Beta measure implementation
    %       zeta = abs(zeta_m*beta_e - zeta_p);
    % 
    %   %     disp('Zeta');
    %   %     disp(zeta);
    %   %     fprintf('Zeta: %f\n', zeta);
    %       fprintf('%f & %f & %f & %2.4f\n', zeta_p, zeta_m, zeta, zeta*100);
    % 
    %       Zeta(end+1) = zeta;
    % 
    %     end
    % 
    %     hold all;
    %     plot(stocks_date, market_index, 'k');
    %     hold off;
    % 
    % 
    %   %   fprintf('Zeta atskirai: %f %f %f\n', Zeta);
    %   %   disp(Zeta);
    %   %   disp('Zeta bendrai');
    %     fprintf('Zeta total: %f\n', sum(Zeta)/length(Zeta) );
    %   %   disp(sum(Zeta)/length(Zeta));
    % 
    %   end
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

    %% Kappa

    % clear bank;
    % for bank = banks
    %   
    %   Kappa = [];
    % 
    % 	bank_dates = dates(bank,:);
    % 	bank_prices = prices(bank,:);
    % 
    % 	for i = 1:length(bank_dates)
    %     
    %     kappa = 0;
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
    %     kappa = (bank_price - stocks_close(start_index))/stocks_close(start_index);
    % 
    %     Kappa(end+1) = abs(kappa);
    % 
    %   end
    %   
    %   disp('Bankas');
    %   disp(colors(bank));
    %   disp(Kappa);
    %   
    %   disp(sum(Kappa)/length(Kappa));
    % 
    % end
end