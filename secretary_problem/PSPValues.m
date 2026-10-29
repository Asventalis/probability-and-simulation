function [y] = PSPValues(n)
% Ritorna le probabilità per i valori da 1 a n
y = zeros(1,double(n));
for k = 1:n
   y(k) = PSP(n,k);
end
end

