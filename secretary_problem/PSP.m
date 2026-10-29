function [prob] = PSP(n,k)
% Probabilità di trovare la migliore moglie tra n avendo ucciso le prime k
prob = k/n*sum(1./(k:n-1));
end

