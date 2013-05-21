% load stocks;
disp('Loading stocks');
stocks = loadjson(file_path{:});
disp('.');
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