SELECT c.client_id,c.sex,c.birth_date,c.district_id,
                  COUNT(DISTINCT d.account_id) AS accounts,
                  COUNT(DISTINCT l.loan_id) AS loans
                  FROM clients c LEFT JOIN disp d ON c.client_id=d.client_id AND d.type='所有者'
                  LEFT JOIN loans l ON d.account_id=l.account_id
                  GROUP BY c.client_id,c.sex,c.birth_date,c.district_id