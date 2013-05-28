%% Zeta

% A little help for the construction of market
disp('impact_to_market');

clear bank;
  
for bank=1:length(banks)
    bank_name = banks(bank);

    Zeta = [];
    bank_dates = dates(bank);
    if iscell(bank_dates)
        bank_dates = bank_dates{:};
    end

    bank_prices = prices(bank);
    if iscell(bank_prices)
        bank_prices = bank_prices{:};
    end

    for i = 1:length(bank_dates)
        market_change = 0;
        stock_change = 0;

        bank_date = bank_dates(i);
        bank_price = bank_prices(i);

        start_index = find(stocks_date==bank_date);
        start_market_index = find(markets_date==bank_date);
        end_index = start_index + 1;
        if end_index > length(stocks_date)
            end_index = length(stocks_date) - 1;
        end

        end_market_index = start_market_index + 1;
        if end_market_index > length(markets_date)
            end_market_index = length(end_market_index) - 1;
        end

        for j = start_index:end_index

            stock_change = stock_change + (stocks_close(j-1) - stocks_close(j))/stocks_close(j-1);
        end

        for j = start_market_index:end_market_index
            if strcmp(bank_name{:}, 'Bank of America') == 1
                disp(['Markets date ', datestr(markets_date(j), 'yyyy-mm-dd')]);
                disp(['Markets close ', num2str(markets_close(j))]);
            end
            market_change = market_change + abs((markets_close(j-1) - markets_close(j))/markets_close(j-1));
        end

        % Beta measure implementation
        zeta = abs(stock_change - market_change*beta_value);
        % fprintf('%f & %f & %f & %2.4f\n', stock_change, market_change, zeta, zeta*100);
        
        if strcmp(bank_name{:}, 'Bank of America') == 1
            disp(['Bank ', bank_name{:}]);
            disp(['Stock change ', num2str(stock_change)]);
            disp(['Market change ', num2str(market_change)]);
            disp(['Stock should change ', num2str(market_change*beta_value)]);
            disp(['Measure ', num2str(abs(stock_change - market_change*beta_value))]);
        end

        Zeta(end+1) = zeta;

    end

    % fprintf('Zeta total: %f\n', sum(Zeta)/length(Zeta) );
    result = sum(Zeta)/length(Zeta);
    if isnan(result)
        result = 0;
    end
    result = round(result*10000)/100;

    global_results{length(global_results)+1} = struct( ...
        'feature', 'impact_to_market', ...
        'analytic', banks(bank), ...
        'ticker', ticker, ...
        'value', result ...
    );

end