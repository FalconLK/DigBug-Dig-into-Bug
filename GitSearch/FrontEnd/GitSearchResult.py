#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GitSearchItem import GitSearchItem
import sys

class GitSearchResult:
	def __init__(self, github_items):
		self.hashes = set() # Set of hashes of snippet in order to avoid duplicate snippet
		self.items = []		# items 안에 있는거 하나를 빼서 item.so_item.title
		self.global_matched_terms = []
		self.load_gitsearch_items(github_items)
		print "GitSearchResult:", len(self.items)
		self.rank_by_multiplication_score()

	def load_gitsearch_items(self, github_items):
		matched_term_acc = set()
		for github_item in github_items:
			print '>>>>>>>>>>>>', github_item.so_item.title
			gitsearch_item = GitSearchItem(github_item)
			gitsearch_item_hash = str(gitsearch_item.github_item.score) # Need some analysis. Is the score unique for each file?

			if gitsearch_item_hash not in self.hashes:
				self.items.append(gitsearch_item)
				print ">>>>>>>>>>>>>>>", gitsearch_item
				self.hashes.add(gitsearch_item_hash)
				matched_term_acc = matched_term_acc.union(gitsearch_item.matched_terms)
			# print gitsearch_item_hash, len(github_items)
		self.global_matched_terms = list(matched_term_acc)

	def sort(self, git_search_score_tuple):
		self.ranked.sort(key=lambda tup: tup[1], reverse=True)

	def rank_by_multiplication_score(self):
		for git_search_item in self.items:
			git_search_item.score = git_search_item.github_item.score * git_search_item.so_item.score
		self.items.sort(key=lambda item: item.score, reverse=True)
