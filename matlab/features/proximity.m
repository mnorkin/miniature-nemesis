%% Beta
disp('Beta');
disp('Proximity')

clear bank;
for bank = 1:length(banks)
  
    Beta = [];

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
        end_index = start_index + 249;
        if end_index > length(stocks_date)-1
            end_index = length(stocks_date);
        end
       
        till_bank_date = stocks_date(end_index);
        
        for ii=1:length(bank_dates)
            check_bank_date = bank_dates(ii);
            if check_bank_date ~= bank_date
                if bank_date < check_bank_date && till_bank_date > check_bank_date
                      till_bank_date = check_bank_date;
                end
            end
        end
        
        end_index = find(stocks_date==till_bank_date);

        beta = 0;

        bank_price = bank_prices(i);

        clear j;

        for j=start_index:end_index-1
            if (stocks_high(j) > bank_price) && (stocks_low(j) > bank_price)
                beta = beta + abs( stocks_high(j) - bank_price )/length(start_index:end_index);
            elseif (stocks_low(j) < bank_price) && (stocks_high(j) < bank_price)
                beta = beta + abs( stocks_low(j) - bank_price )/length(start_index:end_index);
            end
        end
        
        Beta = [Beta beta];

    end

    disp('Bankas');
    % disp(Beta);
    disp(sum(Beta)/length(bank_prices));
    result = sum(Beta)/length(bank_prices);
    if isnan(result)
        result = 0;
    end
    result = round(result*100)/100;

    global_results{length(global_results)+1} = struct( ...
        'feature', 'proximity', ...
        'analytic', banks(bank), ...
        'ticker', ticker, ...
        'value', result ...
      );

end