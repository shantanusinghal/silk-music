# coding=utf-8
import py_entitymatching as em
A = em.load_dataset('person_table_A', key='ID')
B = em.load_dataset('person_table_B', key='ID')
L = em.read_csv_metadata('person_labeled_data.csv', key='_id', ltable=A,
                         rtable=B, fk_ltable='ltable_ID', fk_rtable='rtable_ID')

L1 = em.debug_labeler(L, exclude_attrs=['_id', 'ltable_ID', 'rtable_ID',
                                        'label'], target_attr='label', k=5)

print(L1)
