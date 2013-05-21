 %% Delta
disp('Profitability');
clear bank;
for bank = 1:length(banks)
  
    disp('Bankas');

    Delta = [];

    bank_dates = dates(bank);
    if iscell(bank_dates)
        bank_dates = bank_dates{:};
    end
    bank_prices = prices(bank);
    if iscell(bank_prices)
        bank_prices = bank_prices{:};
    end

    for i = 1:length(bank_dates)

        delta = 0;

        bank_date = bank_dates(i);
        bank_price = bank_prices(i);

        start_index = find(stocks_date==bank_date);
        end_index = start_index + 250;
        if end_index >= length(stocks_date)
            end_index = length(stocks_date) - 1;
        end

        till_bank_date = stocks_date(end_index);

        end_index = find(stocks_date==till_bank_date);

        if stocks_close(start_index) < bank_price
            delta = ( stocks_close(end_index+1) - stocks_close(start_index) ) / stocks_close(start_index);
            disp('Delta');
            disp([num2str(stocks_close(end_index+1)) ' ' num2str(stocks_close(start_index)) ' ' num2str(delta)]);
        else
            delta = ( stocks_close(start_index) - stocks_close(end_index+1) ) / stocks_close(start_index);
            disp('Delta');
            disp([num2str(stocks_close(end_index+1)) ' ' num2str(stocks_close(start_index)) ' ' num2str(delta)]);
        end

        hold all;
        plot([stocks_date(start_index) stocks_date(end_index) ], [stocks_close(start_index) stocks_close(end_index+1) ], ... 
          '-.', 'LineWidth', 3);
        hold off;

        Delta = [Delta delta];
    
    end

    disp('Bankas');
    disp(banks(bank));

    disp(sum(Delta)/length(Delta));
    result = sum(Delta)/length(Delta);
    if isnan(result)
        result = 0;
    end

    result = round(result*100);

    global_results{length(global_results)+1} = struct( ...
        'feature', 'profitability', ...
        'analytic', banks(bank), ...
        'ticker', ticker, ...
        'value', result ...
    );

end