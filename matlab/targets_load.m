% Loading the data
% load dates;
% load prices;
file_path = strcat('target_data/', ticker, '.json');
if exist(file_path{:}, 'file')
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

            hold all;
            plot(bank_date, bank_price, 'x', 'LineWidth', 6);
            hold off;
        end
        get(0,'DefaultAxesColorOrder');
    end
else
    targets = [];
end