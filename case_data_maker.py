import pickle
import html_design


# 案件の基本データを追加保存
def save_new_case_data(case_name, old_url):
    # pk_data = {'kuma': {'url': 'http://kuma-kensetu.com', 'id': 1], 'test': ['http://test.com']}
    with open('data_pickle/case_data.pkl', 'rb') as f:
        pk_data = pickle.load(f)
        if case_name not in pk_data:
            pk_data[case_name] = {'url': old_url}
    print(pk_data)
    with open('data_pickle/case_data.pkl', 'wb') as p:
        pickle.dump(pk_data, p)


if __name__ == '__main__':
    save_new_case_data('iroha_pro', 'http://iroha-pro.com/index.html')
