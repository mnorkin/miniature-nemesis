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