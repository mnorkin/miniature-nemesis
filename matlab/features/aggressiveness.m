%% Kappa

clear bank;
for bank = 1:length(banks)
  
    Kappa = [];

    bank_dates = dates(bank);
    if iscell(bank_dates)
        bank_dates = bank_dates{:}
    end
    bank_prices = prices(bank);
    if iscell(bank_prices)
        bank_prices = bank_prices{:}
    end

    for i = 1:length(bank_dates)
        kappa = 0;

        bank_date = bank_dates(i);
        bank_price = bank_prices(i);

        start_index = find(stocks_date==bank_date);
        end_index = start_index + 250;
        if end_index > length(stocks_date)
            end_index = length(stocks_date) - 1;
        end

        till_bank_date = stocks_date(end_index);
        end_index = find(stocks_date==till_bank_date);
        kappa = (bank_price - stocks_close(start_index))/stocks_close(start_index);
        Kappa(end+1) = abs(kappa);
    end

    disp(sum(Kappa)/length(Kappa));
    result = sum(Kappa)/length(Kappa);
    if isnan(result)
        result = 0;
    end

    result = round(result*10000)/100

    global_results{length(global_results)+1} = struct( ...
        'feature', 'aggressiveness', ...
        'analytic', banks(bank), ...
        'ticker', ticker, ...
        'value', result ...
    );


end